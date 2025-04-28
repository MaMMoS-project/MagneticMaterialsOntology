from graphlib import TopologicalSorter
from astropy import units as u
from ontopy import ontology
from onto_parser import parseObject, OntoObject, canReduce, reduce
import ast

distplayUnits = {
    'MagnetocrystallineAnisotropyConstantK1': 'MJ/m**3'
}

def generateQuantityStatement(name,unit):
  """Generate the quantity statement for a nomad entry.
  @param name: The name of the quantity
  @param unit: The unit of the quantity"""

  keys = [ast.Constant(value='component')]
  values = [ast.Constant(value='NumberEditQuantity')]

  if name in distplayUnits:
    keys.append(ast.Constant(value='defaultDisplayUnit'))
    values.append(ast.Constant(value=distplayUnits[name]))

  keywords = [
      ast.keyword(arg='type', value=ast.Attribute(value=ast.Name(id='np', ctx=ast.Load()), attr='float64', ctx=ast.Load())),
      ast.keyword(arg='a_eln', value=ast.Dict(keys=keys, 
                                              values=values)),
      ast.keyword(arg='unit', value=ast.Constant(value=unit.to_string('vounit', fraction=True)))
    ]
  
  return ast.Assign(
    targets=[ast.Name(id=name, ctx=ast.Store())],
    value=ast.Call(func=ast.Name(id='Quantity', ctx=ast.Load()), args=[], keywords=keywords)
  )

def generateQuantityStatementString(name):
  """Generate the quantity statement for a nomad entry for a String Quanitity.
  @param name: The name of the quantity"""

  keywords = [
      ast.keyword(arg='type', value=ast.Constant(value='str')),
      ast.keyword(arg='a_eln', value=ast.Dict(keys=[ast.Constant(value='component')], 
                                              values=[ast.Constant(value='StringEditQuantity')]))
    ]

  return ast.Assign(
    targets=[ast.Name(id=name, ctx=ast.Store())],
    value=ast.Call(func=ast.Name(id='Quantity', ctx=ast.Load()), args=[], keywords=keywords)
  )


def generateMDef(object: OntoObject) -> ast.Assign:
    """Generate the m_def statement for a nomad entry.

    This entry usually has the following structure:
    `m_def = Section(
        a_eln=dict(
        properties=dict(order=[
            'spaceGroup'
        ])
        )
    )`"""
    props = []
    # create what is inside of 'properties'
    if object.unit is not None or object.isString:
        props.append(ast.Constant(value=object.label))
    for component in object.components:
        props.append(ast.Constant(value=component.label))
    actual_properties = ast.List(elts=props, ctx=ast.Load())
    # create the assign statment
    return ast.Assign(
        targets=[ast.Name(id='m_def', ctx=ast.Store())],
        # it is a call to 'Seciton'
        value=ast.Call(func=ast.Name(id='Section', ctx=ast.Load()),
                   args=[],
                   keywords=[ast.keyword(arg='a_eln',
                                         value=ast.Call(func=ast.Name(id='dict', ctx=ast.Load()),
                                                        args=[],
                                                        keywords=[
                                                            ast.keyword(arg='properties',
                                                                        value=ast.Call(func=ast.Name(id='dict', ctx=ast.Load()),
                                                                                       args=[],
                                                                                       keywords=[
                                                                                           ast.keyword(arg='order',
                                                                                                       value=actual_properties)]))]))]))

def generateSectionStatement(object: OntoObject):
  name = object.name.split('.')[-1]
  funct = ast.Call(func = ast.Name(id='SubSection', ctx=ast.Load()), args=[],
                   keywords=[ast.keyword(arg='section_def', value=ast.Name(id=name, ctx=ast.Load())),
                             ast.keyword(arg='repeats', value=ast.Constant(value=object.repeats))])
  return ast.Assign(targets=[
    ast.Name(id=object.label, ctx=ast.Store())],
    value=funct)

def generateClassDef(object: OntoObject):
    body = [generateMDef(object)]
    if object.unit is not None:
        body.append(generateQuantityStatement(object.label, object.unit))
    elif object.isString:
        body.append(generateQuantityStatementString(object.label))

    if object.components != []:
        for component in object.components:
            body.append(generateSectionStatement(component))

    if body == []:
        body.append(ast.Pass())

    bases = [ast.Name(id="ArchiveSection", ctx=ast.Load())]
    for parent in object.parents:
        name = parent.name.split('.')[-1]
        bases.append(name)

    name = object.name.split('.')[-1]
    # print(name, body)
    return ast.ClassDef(
            name=name,
            bases=bases,
            keywords=[],
            body=body,
            decorator_list=[]
    )

def test(ontology, label):
    obj = ontology.get_by_label(label)
    # print(obj, type(obj))
    obb = parseObject(obj)

    module = ast.Module(body=[], type_ignores=[])
    module.body.append(generateClassDef(obb))

    ast.fix_missing_locations(module)
    _ = compile(module, filename="<ast>", mode="exec")

    print(ast.unparse(module))

    print(canReduce(obb))
    if canReduce(obb):
        reducedObb = reduce(obb)
        print('\nReduced', reducedObb, "reduced unit = '%s'" % reducedObb.unit.to_string('vounit', fraction=True) if 
              reducedObb.unit is not None else 'None')
    else:
        print('\nNot Reduced', obb.name, obb.parents)

def test2(entry):
    obb = parseObject(entry)

    module = ast.Module(body=[], type_ignores=[])
    module.body.append(generateClassDef(obb))

    ast.fix_missing_locations(module)
    _ = compile(module, filename="<ast>", mode="exec")

    print(ast.unparse(module))

    print(canReduce(obb))
    if canReduce(obb):
        reducedObb = reduce(obb)
        print('\nReduced', reducedObb, "reduced unit = '%s'" % reducedObb.unit.to_string('vounit', fraction=True) if 
              reducedObb.unit is not None else 'None')
    else:
        print('\nNot Reduced', obb.name, obb.parents)


def flatten(obj: OntoObject) -> list[OntoObject]:
    if obj.parents == [] and obj.components == []:
        return [obj.name]
    else:
        ret = [obj.name]
        for parent in obj.parents:
            ret.extend(flatten(parent))
        for component in obj.components:
            ret.extend(flatten(component))
        return ret

class Generator:
    def __init__(self, ontology, output=None, base=None):
        self.ontology = ontology
        self.output = output
        self.baseFile = base
        self.entries = []
        self.entryMap = {}
    
    def addObject(self, label):
        entry = self.ontology.get_by_label(label)
        obb = parseObject(entry)

        if canReduce(obb):
          reducedObb = reduce(obb)
          print('\nReduced', reducedObb, "reduced unit = '%s'" % reducedObb.unit.to_string('vounit', fraction=True) if 
                reducedObb.unit is not None else 'None')
          self.entries.append(reducedObb)
        else:
            print('\nNot Reduced', obb.name, obb.parents)
            self.entries.append(obb)

    def generate(self):
        entities = set()
        for entry in self.entries:
            for e in flatten(entry):
              print(e)
              entities.add(e)

        print('Entities', entities)

        self.buildEntryMap()
        sorted_entries = self.buildDependencyGraph()
        
        if self.baseFile is not None:
            # Either append the definition to 'nomad_base.py' code
            module = ast.parse(open(self.baseFile,'r').read())
        else:
            module = ast.Module(body=[], type_ignores=[])
        module = ast.Module(body=[], type_ignores=[])
        for name in sorted_entries:
            module.body.append(generateClassDef(self.entryMap[name]))

        ast.fix_missing_locations(module)
        _ = compile(module, filename="<ast>", mode="exec")

        out = ast.unparse(module)
        print(out)

        if self.output is not None:
            with open(self.output, 'w') as f:
                f.write(out)
                f.close()

    def buildEntryMap(self):
        def entryToMap(entryMap: dict, entry: OntoObject):
            for parent in entry.parents:
                entryToMap(entryMap, parent)
            for component in entry.components:
                entryToMap(entryMap, component)
            entryMap[entry.name] = entry

        for entry in self.entries:
            entryToMap(self.entryMap, entry)
    
    def buildDependencyGraph(self):
        def depencenciesToGraph(graph, entry: OntoObject):
            for parent in entry.parents:
                depencenciesToGraph(graph, parent)
            for component in entry.components:
                depencenciesToGraph(graph, component)
            dependencies = []
            dependencies.extend([parent.name for parent in entry.parents])
            dependencies.extend([component.name for component in entry.components])
            graph[entry.name] = dependencies

        graph = {}
        for entry in self.entries:
            depencenciesToGraph(graph, entry)

        ts = TopologicalSorter(graph)
        sorted_entries = tuple(ts.static_order())
        print(f'Sorted entries {sorted_entries}')

        return sorted_entries

def generateClasses(output: str, base: str, classes: list[str]):
    """Generate the classes for the given classes.

    @param output: The output file
    @param base: The base file to include in the generated code
    @param classes: The classes to generate"""

    # Load the local stored ontology file
    hugo = ontology.get_ontology('./magnetic_material_mammos.ttl')
    hugo.load()

    generator = Generator(hugo,output, base)
    for clasz in classes:
        generator.addObject(clasz)

    generator.generate()

def generateOnto(output: str, base: str):
    """Generate the classes for the given ontology.

    @param output: The output file
    @param base: The base file to include in the generated code"""

    import build_onto

    # Load the local stored ontology file
    hugo = ontology.get_ontology('./magnetic_material_mammos.ttl')
    hugo.load()

    generator = Generator(hugo,output,str)

    for entry in dir(build_onto):
        # TODO: this is a very stupid workaround! Shame on you Martin
        if entry == "__builtins__":
            break
        # and the stupid workarounds continue
        if entry in ['Not','AnnotationProperty','World']:
            continue
        # TODO code should be aware that all of these are AnnotationProperty and thus ignore it (instead of black listing)
        if entry in ['IECEntry', 'wikipediaReference','wikidataReference']:
            continue

        print('Processing', entry)
        generator.addObject(entry)
    generator.generate()


if __name__ == "__main__":
    import argparse

    # Parse options
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', help='Output file', default='generated.py')
    parser.add_argument('--base', help='Base file to include in the generated code', default=None)
    #optional list for classes to generate
    parser.add_argument('--classes', help='Classes to generate', nargs='+', default=None)

    args = parser.parse_args()

    if args.classes != []:
        generateClasses(args.output, args.base, args.classes)