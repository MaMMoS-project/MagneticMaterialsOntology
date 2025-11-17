import argparse
import ast
from graphlib import TopologicalSorter
import inspect
import re
from astropy import units as u
import owlready2


# Load ontology
import build_onto

# TODO: entities directly from the emmo. We need this for IntrinsicMagneticProperties, where there is is_a emmo.hasProperty.some(emmo.CurieTemperature)


def auto_str(cls):
    def __str__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )

    cls.__str__ = __str__
    return cls


@auto_str
class GeneratedClass:
    def __init__(self):
        self.dependencies = []

    def __repr__(self):
        return self.__str__()


class DepencencyGraph:
    def __init__(self):
        self.dependencies = {}
        self.generated = []

    def __str__(self):
        return (
            "DepencencyGraph(dependencies={"
            + "\n".join([""] + [f"  '{k}': {v}" for k, v in self.dependencies.items()])
            + "}"
            + f", generated = {self.generated})"
        )


graph = DepencencyGraph()


def dependencyToClassName(dependency: str) -> str:
    if dependency.startswith("emmo-inferred."):
        className = dependency[14:]
    elif dependency.startswith("magnetic_material."):
        className = dependency[18:]
    elif dependency.startswith("emmo."):
        className = dependency[5:]
    else:
        className = dependency

    return className


def generateMDef(props=["k1"]):
    """Generate the m_def statement for a nomad entry.

    This entry usually has the following structure:
    `m_def = Section(
      a_eln=dict(
        properties=dict(order=[
          'spaceGroup'
        ])
      )
    )`"""
    # create what is inside of 'properties'
    actual_properties = ast.List(elts=[ast.Constant(value=props[0])], ctx=ast.Load())
    # create the assign statement
    return ast.Assign(
        targets=[ast.Name(id="m_def", ctx=ast.Store())],
        # it is a call to 'Section'
        value=ast.Call(
            func=ast.Name(id="Section", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(
                    arg="a_eln",
                    value=ast.Call(
                        func=ast.Name(id="dict", ctx=ast.Load()),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="properties",
                                value=ast.Call(
                                    func=ast.Name(id="dict", ctx=ast.Load()),
                                    args=[],
                                    keywords=[
                                        ast.keyword(
                                            arg="order", value=actual_properties
                                        )
                                    ],
                                ),
                            )
                        ],
                    ),
                )
            ],
        ),
    )


def generateQuantityStatement(name, unit, isString):
    """Generate the quantity statement for a nomad entry.
    @param name: The name of the quantity
    @param unit: The unit of the quantity. If None, then isString is supposed to be True
    @param isString: If the quantity is a string. If true unit is supposed to be None"""

    # TODO: hasMeterologicalReference only MeasurementUnit is not treated correctly. ISO80000 (CondencesMatterPhysicsQuantity) is not treated correctly
    # TODO: some Quantities are generated empty - is this a problem?

    # Unit is supposed to be not none and an astropy unit
    if unit is not None:
        keywords = [
            ast.keyword(
                arg="type",
                value=ast.Attribute(
                    value=ast.Name(id="np", ctx=ast.Load()),
                    attr="float64",
                    ctx=ast.Load(),
                ),
            ),
            ast.keyword(
                arg="a_eln",
                value=ast.Dict(
                    keys=[ast.Constant(value="component")],
                    values=[ast.Constant(value="NumberEditQuantity")],
                ),
            ),
            ast.keyword(
                arg="unit",
                value=ast.Constant(value=unit.to_string("vounit", fraction=True)),
            ),
        ]
    elif isString:
        keywords = [
            ast.keyword(arg="type", value=ast.Name(id="str", ctx=ast.Load())),
            ast.keyword(
                arg="a_eln",
                value=ast.Dict(
                    keys=[ast.Constant(value="component")],
                    values=[ast.Constant(value="StringEditQuantity")],
                ),
            ),
        ]
    else:
        keywords = []
    return ast.Assign(
        targets=[ast.Name(id=name, ctx=ast.Store())],
        value=ast.Call(
            func=ast.Name(id="Quantity", ctx=ast.Load()), args=[], keywords=keywords
        ),
    )


def generateClassDef(name, attrname, unit=None, isString=False):
    return ast.ClassDef(
        name=name,
        bases=[ast.Name(id="ArchiveSection", ctx=ast.Load())],
        keywords=[],
        body=[
            generateMDef([attrname]),
            generateQuantityStatement(attrname, unit, isString),
        ],
        decorator_list=[],
    )


def generateSubsectionStatement(name, type, repeats=False):
    funct = ast.Call(
        func=ast.Name(id="SubSection", ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg="section_def", value=ast.Name(id=type, ctx=ast.Load())),
            ast.keyword(arg="repeats", value=ast.Constant(value=repeats)),
        ],
    )
    return ast.Assign(targets=[ast.Name(id=name, ctx=ast.Store())], value=funct)


def generateClassDefComplex(name, attrname, obj):
    body = [generateMDef([attrname])]
    bases = [ast.Name(id="ArchiveSection", ctx=ast.Load())]

    attr = getattr(obj, "is_a")

    dependencies = []

    # Things for which we do not want to generate something
    filter = ["owl.Thing", "Thing"]

    for x in attr:
        whiteList = [
            # entry is a restriction , and
            type(x) is owlready2.class_construct.Restriction
            and (
                # either a dimension string i.e. it tells us which unit it is
                str(x.property).find("hasDimensionString") != -1
                or str(x.property).find("hasMeasurementUnit") != -1
                or str(x.property).find("hasProperty") != -1
            ),
            type(x) is owlready2.entity.ThingClass,
        ]

        if not any(whiteList):
            print(x, "is not white listed")
            continue

        if type(x) is owlready2.class_construct.Restriction:
            namestr = str(x.value)
            # eval('build_onto.' + namestr.split('.')[-1])
            typeT = namestr.split(".")[-1]
            strProp = str(x.property).replace("emmo-inferred.", "")
            print(
                f"Parsing restriction to {namestr}. typeT {typeT} strProp {strProp} classes {hasattr(x.value, 'Classes')}"
            )
            if strProp == "hasDimensionString":
                unit = convert_to_iso_unit(typeT)
                # print('attrname', attrname)
                print(
                    attrname,
                    "converted to unit",
                    unit,
                    unit.to_string("vounit", fraction=True),
                )

                # print(ast.unparse(code))
                body.append(
                    generateQuantityStatement(
                        attrname, convert_to_iso_unit(typeT), isString=False
                    )
                )
            else:
                # Now we need to check if this is a hasProperty.TYPE restriction
                #  if it is hasProperty.min, then type == 27. We need to have this option to treat min(0,....) as repeats=True
                repeats = (
                    True
                    if hasattr(x, "cardinality")
                    and x.cardinality is not None
                    and (x.cardinality > 1 or x.get_typename() == "min")
                    else False
                )

                # Check if this restriction is a restriction to a single class or to multiple classes
                # if it does not have classes, it is to a single class.
                # if it has classes, it is to multiple classes. --> In Nomad we cannot do this, so we create a SubSection for each class
                if not hasattr(x.value, "Classes"):
                    subobj = build_onto.onto.get_by_label(typeT)
                    quantName = (
                        subobj.get_preferred_label()[:]
                        if hasattr(obj, "altLabel")
                        else "value"
                    )
                    body.append(
                        generateSubsectionStatement(quantName, typeT, repeats=repeats)
                    )
                    dependencies.append(typeT)
                else:
                    for alternative in x.value.Classes:
                        # print('y', alternative)
                        typeT = str(alternative).split(".")[-1]
                        subobj = build_onto.onto.get_by_label(typeT)
                        quantName = (
                            subobj.get_preferred_label()[:]
                            if hasattr(obj, "altLabel")
                            else "value"
                        )
                        body.append(
                            generateSubsectionStatement(
                                quantName, typeT, repeats=repeats
                            )
                        )
                        dependencies.append(str(alternative))
        elif type(x) is owlready2.entity.ThingClass:
            # TODO: hier waere es gut, wenn gecheckt werden kann, ob die einzelnen dependencies nicht leer sind - also keinen weiteren Informationsgehalt bieten

            dep = str(x)
            if dep not in filter:
                dependencies.append(str(x))
                className = str(x).split(".")[-1]
                bases.append(ast.Name(id=className, ctx=ast.Load()))

    dependencies = [d for d in dependencies if d not in filter]

    return (
        ast.ClassDef(name=name, bases=bases, keywords=[], body=body, decorator_list=[]),
        dependencies,
    )


def convert_to_iso_unit(unit_string):
    """Converts a string representation of ISQ base quantities to its ISO unit symbols using astropy.

    Args:
        unit_string: The string representation of the ISQ base quantities.

    Returns:
        The ISO unit symbols as astropy object.
    """

    unit_map = {
        "T": "s",
        "L": "m",
        "M": "kg",
        "I": "A",
        "Θ": "K",
        "N": "mol",
        "J": "cd",
    }

    # Parse the unit string into a list of (base_unit, exponent) tuples
    units = re.findall(r"([TLMIΘNJ])([+-]?\d+)", unit_string)

    # Create the astropy unit
    astropy_unit = 1
    for base_unit, exponent in units:
        if exponent:
            astropy_unit *= getattr(u, unit_map[base_unit]) ** int(exponent)
        else:
            astropy_unit *= getattr(u, unit_map[base_unit])
    return u.Unit(astropy_unit)


def getUnit(entity):
    class_prop = entity.get_class_properties()
    # print(class_prop)
    if build_onto.emmo.hasMeasurementUnit in list(class_prop):
        print("Measurement unit property found for class", entity.hasMeasurementUnit[0])
        try:
            return u.Unit(entity.hasMeasurementUnit[0])
        except Exception as e:
            print(f"Error: {e}")
            return None
    else:
        # print(f'Measurement unit property not found for class {entity}. Unit for {entity} is inherited.')
        C_emmo = list(entity.get_parents())[0]
        # print(f'Parent class of {entity} is: {C_emmo}')
        try:
            # print('Measurement unit property found for parent class of ' + entity.label)
            mfs_unit = C_emmo.hasMeasurementUnit[0]
            # print(f'Measurement unit of parent class of {entity} is: {mfs_unit}')
            # print(type(mfs_unit), mfs_unit.ucumCode)

            if mfs_unit.ucumCode != []:
                return u.Unit(mfs_unit.ucumCode[0])
            else:
                return convert_to_iso_unit(mfs_unit.hasDimensionString)
        except:
            print(f"Measurement unit property not found for parent class of {entity}")
            return None


def generateForName(entry, emmo=False):
    # Create an instance of the object from the onotolgy
    # obj = eval(f'build_onto.{entry}') # TODO: move to `obj = build_onto.emmo.get_(entry)`
    # but this does currently not work for 'MainPhase`.
    if emmo:
        # import emmo
        obj = eval(f"build_onto.emmo.{entry}")
        fullName = "emmo." + entry
    else:
        obj = eval(f"build_onto.{entry}")
        fullName = entry

    return generateForObject(obj, entry, fullName)


def generateForObject(obj, entry, fullName):
    quantName = obj.get_preferred_label()[:] if hasattr(obj, "altLabel") else "value"

    # supers = inspect.getmro(eval('build_onto.' + entry))
    # print(entry, 'emmo-inferred.NominalProperty' in supers, magnetic_material.EnergyDensity in supers, supers, type(supers[0]), supers[1])
    # print(entry, supers)

    # obj = eval('build_onto.' + entry)
    isString = False
    isComplex = False
    if hasattr(obj, "is_a"):
        attr = getattr(obj, "is_a")
        print(obj, type(attr[0]), attr)
        if len(attr) >= 1:
            if len(attr) > 1:
                print(
                    obj,
                    "is complex",
                    attr,
                    type(attr[1]),
                    type(attr[1]) is owlready2.class_construct.Restriction,
                )
            for x in attr:
                # The following line could replace the x.type == 24 hack. (It works for what we've tested so far)
                # WARNING: distinguish whether it's magnetic_material or emmo. If emmo then do the same as the hack above
                # type(eval('build_onto.' + str(x.value).split('.')[-1] + '.hasStringValue')) is not NoneType
                if hasattr(x, "type") and x.type == 24:
                    isString = True
            if not isString:
                print(len(attr))
            isComplex = True
            # x = attr[1]
            # namestr = str(x.value)
            # eval('build_onto.' + namestr.split('.')[-1])
    else:
        print(obj, "has no is_a")
        pass

    # print(f"My current test {entry} {str(entry)} {str(entry).startswith('magnetic_material')} complex {isComplex} string {isString}")

    unit = getUnit(obj)
    # if unit is not None:
    #   print(obj, unit)
    # else:
    #   print(obj, "has no unit")
    print(
        f"obj {obj}, entry {entry} unit:{unit}, string:{isString} complex {isComplex}"
    )

    if isComplex:
        ret, dependencies = generateClassDefComplex(entry, quantName, obj)
    else:
        ret = generateClassDef(entry, quantName, unit, isString)
        dependencies = []
    # ret = None

    graph.generated.append(fullName)
    if fullName not in graph.dependencies:
        graph.dependencies[fullName] = GeneratedClass()
    print("  Adding dependencies for", fullName, dependencies)
    graph.dependencies[fullName].dependencies = dependencies
    graph.dependencies[fullName].code = ret

    return ret


def generateMissing(module, depth=0):
    """Generate all entries which are missing (as some already generated entries depend on it)

    @param depth can be ignored by users. Is might be used to limit the recursion depth (during testing it was not necessary)"""
    entries = set(list(graph.dependencies.keys()))
    generateMissingEntries(module, entries)
    print("\nDiff", list(set(list(graph.dependencies.keys())) - entries))
    if list(set(list(graph.dependencies.keys())) - entries) != []:
        print("\n\n\n\n\nStupid recursion", depth)
        generateMissing(module, depth=depth + 1)


def generateMissingEntries(module, entries):
    """Helper-function to actually generate the entries. Users should not call this function."""
    for entry in entries:
        for dependency in graph.dependencies[entry].dependencies:
            # dependency is a fullName
            if (
                dependency not in graph.generated
                and dependencyToClassName(dependency) not in graph.dependencies
            ):
                print(
                    f"Generating missing class {dependency} generated: {graph.generated}, graphkeys:{graph.dependencies.keys()}"
                )
                className = dependencyToClassName(dependency)
                module.body.append(
                    generateForObject(
                        build_onto.emmo.get_by_label(className),
                        className,
                        fullName=dependency,
                    )
                )


def cleanGraphEmmoInferred(graph):
    entries = list(graph.dependencies.items())
    for name, entry in entries:
        if name.startswith("emmo-inferred"):
            del graph.dependencies[name]
            graph.dependencies[name.replace("emmo-inferred", "emmo")] = entry
        entry.dependencies = [
            dependency
            if not dependency.startswith("emmo-inferred")
            else dependency.replace("emmo-inferred", "emmo")
            for dependency in entry.dependencies
        ]


def main(output, baseFile=None):
    if baseFile is not None:
        # Either append the definition to 'nomad_base.py' code
        module = ast.parse(open(baseFile, "r").read())
    else:
        module = ast.Module(body=[], type_ignores=[])

    for entry in dir(build_onto):
        # TODO: this is a very stupid workaround! Shame on you Martin
        if entry == "__builtins__":
            break
        # and the stupid workarounds continue
        if entry in ["Not", "AnnotationProperty", "World"]:
            continue
        # TODO code should be aware that all of these are AnnotationProperty and thus ignore it (instead of black listing)
        if entry in ["IECEntry", "wikipediaReference", "wikidataReference"]:
            continue

        print("Processing", entry)
        module.body.append(generateForName(entry))

    # Or create standalone code
    # module = ast.Module(body=[k1],type_ignores=[])

    # module.body.append(generateForName('MagnetocrystallineAnisotropyConstantK1'))
    # module.body.append(generateForName('SpaceGroup'))
    # module.body.append(generateForName('CoercivityHc'))
    # module.body.append(generateForName('CrystalStructure'))
    # module.body.append(generateForName('IntrinsicMagneticProperties'))
    # module.body.append(generateForName('CurieTemperature', emmo=True))
    # module.body.append(generateForName('CriticalTemperature', emmo=True))
    # module.body.append(generateForName('CondensedMatterPhysicsQuantity', emmo=True))

    # module.body.append(generateForName("ExchangeStiffnessConstant"))
    # module.body.append(generateForName('AbsolutePermeability'))
    # module.body.append(generateForName('AmpereSquareMetrePerKilogram'))
    # module.body.append(generateForName('AmorphousMagneticMaterial'))
    # module.body.append(generateForName('GranularStructure'))
    # module.body.append(generateForName('MagnetocrystallineAnisotropy'))
    # module.body.append(generateForName('MainPhase'))
    # module.body.append(generateForName('KneeField'))
    # module.body.append(generateForName('MagneticPolarisation', emmo=True))

    generateMissing(module)

    # ast.fix_missing_locations(module)
    # _ = compile(module, filename="<ast>", mode="exec")
    # print(ast.unparse(module))

    print(graph)

    # with open(output, 'w') as f:
    #   f.write(ast.unparse(module))
    #   f.close()

    # sort graph by requiredFrom in descending order
    # sorted_graph = sorted(graph.dependencies.items(), key=lambda x: x[1].requiredFrom, reverse=True)
    # print('Sorted graph:', sorted_graph)

    if baseFile is not None:
        # Either append the definition to 'nomad_base.py' code
        module = ast.parse(open(baseFile, "r").read())
    else:
        module = ast.Module(body=[], type_ignores=[])

    # for (key,obj) in graph.dependencies.items():
    #   module.body.append(obj.code)

    # clean the graph
    # entries = list(graph.dependencies.items())
    # for (name,entry) in entries:
    #   className = dependencyToClassName(name)
    #   if name != className and className in graph.dependencies:
    #     print(f'Found {name} and {className} in the graph. Removing {name} {hasattr(graph.dependencies[name], "code")} {hasattr(graph.dependencies[className],"code")}')
    #     # del graph.dependencies[name]
    cleanGraphEmmoInferred(graph)

    # check graph
    print("")
    entries = list(graph.dependencies.items())
    for name, entry in entries:
        className = dependencyToClassName(name)
        if name != className and className in graph.dependencies:
            print(f"Found {name} and {className} in the graph.")
    print("")

    # turn graph into dict
    dict_graph = {
        dependencyToClassName(k): [
            dependencyToClassName(name) for name in v.dependencies
        ]
        for k, v in graph.dependencies.items()
    }
    # dict_graph = {k: [name for name in v.dependencies] for k, v in graph.dependencies.items()}
    mapping = {}
    for k, v in graph.dependencies.items():
        for name in v.dependencies:
            mapping[dependencyToClassName(name)] = name
        mapping[dependencyToClassName(k)] = k

    print(f"Dict graph {dict_graph}")
    print(f"Mapping: {mapping}")

    ts = TopologicalSorter(dict_graph)
    sorted_entries = tuple(ts.static_order())
    print(f"Sorted entries {sorted_entries}")
    for entry in sorted_entries:
        # if entry not in graph.dependencies:
        #   print(f'Why is {entry} not in the graph????')
        #   continue
        # if not hasattr(graph.dependencies[entry],'code'):
        #   print(f'Why does {entry} have no code???')
        #   continue
        # module.body.append(graph.dependencies[entry].code)
        ee = mapping[entry]
        if ee not in graph.dependencies:
            if entry not in graph.dependencies:
                print(f"Why is {ee}/{entry} not in the graph????")
                continue
            else:
                ee = entry  # In some cases it does not exist in the 'qualified' version but in the plain
                # if this is the case, we can use it.
        if not hasattr(graph.dependencies[ee], "code"):
            print(f"Why does {ee}/{entry} have no code???")
            continue
        module.body.append(graph.dependencies[ee].code)

    ast.fix_missing_locations(module)
    _ = compile(module, filename="<ast>", mode="exec")

    with open(output, "w") as f:
        f.write(ast.unparse(module))
        f.close()


if __name__ == "__main__":
    # Parse options
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Output file", default="generated.py")
    parser.add_argument(
        "--base", help="Base file to include in the generated code", default=None
    )

    args = parser.parse_args()

    main(args.output, args.base)
