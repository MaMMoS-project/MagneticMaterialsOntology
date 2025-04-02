import ast
import inspect
import re
from astropy import units as u
import owlready2

# TODO: entitites direkt aus dem emmo. Brauchen wir fuer IntrinsicMagneticProperties, dort gibt es bei is_a emmo.hasProperty.some(emmo.CurieTemperature)

def auto_str(cls):
  def __str__(self):
    return '%s(%s)' % (
        type(self).__name__,
        ', '.join('%s=%s' % item for item in vars(self).items())
    )
  cls.__str__ = __str__
  return cls

@auto_str
class GeneratedClass:
  def __init__(self):
    self.dependencies = []

@auto_str
class DepencencyGraph:
  def __init__(self):
    self.dependencies = {}
    self.generated = []

graph = DepencencyGraph()

def generateMDef(props=['k1']):
  # create what is inside of 'properties'
  actual_properties = ast.List(elts=[ast.Constant(value=props[0])], ctx=ast.Load())
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

def generateQuantityStatement(name,unit,isString):
  # TODO: hasMeterologicalReference only MeasurementUnit is not treated correctly. ISO80000 (CondencesMatterPhysicsQuantity) is not treated correctly
  if unit is not None:
    keywords = [
      ast.keyword(arg='type', value=ast.Attribute(value=ast.Name(id='np', ctx=ast.Load()), attr='float64', ctx=ast.Load())),
      ast.keyword(arg='a_eln', value=ast.Dict(keys=[ast.Constant(value='component')], 
                                              values=[ast.Constant(value='NumberEditQuantity')])),
      ast.keyword(arg='unit', value=ast.Constant(value=unit.to_string('vounit', fraction=True)))
    ]
  elif isString:
    keywords = [
      ast.keyword(arg='type', value=ast.Name(id='str', ctx=ast.Load())),
      ast.keyword(arg='a_eln', value=ast.Dict(keys=[ast.Constant(value='component')],
                                              values=[ast.Constant(value='StringEditQuantity')]))
    ]
  else:
    keywords = []
  return ast.Assign(
    targets=[ast.Name(id=name, ctx=ast.Store())],
    value=ast.Call(func=ast.Name(id='Quantity', ctx=ast.Load()), args=[], keywords=keywords)
  )

def generateClassDef(name,attrname,unit=None,isString=False):
  return ast.ClassDef(
            name=name,
            bases=[ast.Name(id="ArchiveSection", ctx=ast.Load())],
            keywords=[],
            body=[
              generateMDef([attrname]),
              generateQuantityStatement(attrname,unit,isString)],
            decorator_list=[]
  )

def generateSubsectionStatement(name, type,repeats=False):
  funct = ast.Call(func = ast.Name(id='SubSection', ctx=ast.Load()), args=[],
                   keywords=[ast.keyword(arg='section_def', value=ast.Name(id=type, ctx=ast.Load())),
                             ast.keyword(arg='repeats', value=ast.Constant(value=repeats))])
  return ast.Assign(targets=[
    ast.Name(id=name, ctx=ast.Store())],
    value=funct)

def generateClassDefComplex(name,attrname,obj):
  body = [generateMDef([attrname])]
  bases = [ast.Name(id="ArchiveSection", ctx=ast.Load())]

  attr = getattr(obj, 'is_a')

  dependencies = []

  for x in attr:
    if hasattr(x, 'label') and len(x.label) > 0 and x.label[0][:] == 'Property' or str(x).find('.hasSIConversionMultiplier') != -1 or str(x).find('.hasSIConversionOffset') != -1 or str(x).find('.unitSymbolValue') != -1: 
      continue
    # print(f'x: {x} {str(x)} {attr} hasAttr(value):{hasattr(x, "value")} isRestriction:{type(attr[1]) is owlready2.class_construct.Restriction}')

    if type(x) is owlready2.class_construct.Restriction:
      ss = str(x)
      if ss.find('.hasSIConversionMultiplier') != -1:
        print('hasSIConversionMultiplier')
        continue
      namestr = str(x.value)
      # eval('build_onto.' + namestr.split('.')[-1])
      typeT = namestr.split('.')[-1]
      strProp = str(x.property).replace('emmo-inferred.','')
      print(f'Parsing restriction to {namestr}. typeT {typeT} strProp {strProp} classes {hasattr(x.value,"Classes")}')
      if strProp == 'hasDimensionString':
        unit = convert_to_iso_unit(typeT)
        print('attrname', attrname)
        print('converted to unit', unit, unit.to_string('vounit', fraction=True))

        # print(ast.unparse(code))
        body.append(generateQuantityStatement(attrname,convert_to_iso_unit(typeT),isString=False))
      else:
        # Now we need to check if this is a hasProperty.TYPE restriction
        #  if it is hasProperty.min, then type == 27. We need to have this option to treat min(0,....) as repeats=True
        repeats = True if hasattr(x, 'cardinality') and x.cardinality is not None and (x.cardinality > 1 or x.get_typename() == 'min') else False

        # Check if this restriction is a restriction to a single class or to multiple classes
        # if it does not have classes, it is to a single class.
        # if it has classes, it is to multiple classes. --> In Nomad we cannot do this, so we create a SubSection for each class
        if not hasattr(x.value, 'Classes'):
          subobj = build_onto.onto.get_by_label(typeT)
          quantName = subobj.get_preferred_label()[:] if hasattr(obj,'altLabel') else 'value'
          body.append(generateSubsectionStatement(quantName, typeT, repeats=repeats))
          dependencies.append(typeT)
        else:
          for alternative in x.value.Classes:
            print('y', alternative)
            typeT = str(alternative).split('.')[-1]
            subobj = build_onto.onto.get_by_label(typeT)
            quantName = subobj.get_preferred_label()[:] if hasattr(obj,'altLabel') else 'value'
            body.append(generateSubsectionStatement(quantName, typeT, repeats=repeats))
          dependencies.append(typeT)
    else:
      # TODO: der name muss noch korrekt werden --> x = magnetic_material.MagneticMaterial
      dependencies = [str(x)]
      bases.append(ast.Name(id=str(x), ctx=ast.Load()))

  graph.dependencies[name] = GeneratedClass()
  graph.dependencies[name].dependencies = dependencies

  return ast.ClassDef(
            name=name,
            bases=bases,
            keywords=[],
            body=body,
            decorator_list=[]
  )

def convert_to_iso_unit(unit_string):
    """Converts a string representation of ISQ base quantities to its ISO unit symbols using astropy.

    Args:
        unit_string: The string representation of the ISQ base quantities.

    Returns:
        The ISO unit symbols as astropy object.
    """

    unit_map = {
        'T': 's',
        'L': 'm',
        'M': 'kg',
        'I': 'A',
        'Θ': 'K',
        'N': 'mol',
        'J': 'cd'
    }

    # Parse the unit string into a list of (base_unit, exponent) tuples
    units = re.findall(r'([TLMINJ])([+-]?\d+)', unit_string)

    # Create the astropy unit
    astropy_unit = 1
    for base_unit, exponent in units:
        if exponent:
            astropy_unit *= getattr(u, unit_map[base_unit])**int(exponent)
        else:
            astropy_unit *= getattr(u, unit_map[base_unit])
    return u.Unit(astropy_unit)

def getUnit(entity):
  class_prop = entity.get_class_properties()
  # print(class_prop)
  if build_onto.emmo.hasMeasurementUnit in list(class_prop):
    print('Measurement unit property found for class', entity.hasMeasurementUnit[0])
    try:
      return u.Unit(entity.hasMeasurementUnit[0])
    except Exception as e:
      print(f'Error: {e}')
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
      print(f'Measurement unit property not found for parent class of {entity}')
      return None




def generateForName(entry, hack=False):
  # Create an instance of the object from the onotolgy
  # obj = eval(f'build_onto.{entry}') # TODO: move to `obj = build_onto.emmo.get_(entry)`
  # but this does currently not work for 'MainPhase`.
  if hack:
    # import emmo
    obj = eval(f'build_onto.emmo.{entry}')
  else:
    obj = eval(f'build_onto.{entry}')
  
  return generateForObject(obj, entry)

def generateForObject(obj, entry):
  quantName = obj.get_preferred_label()[:] if hasattr(obj,'altLabel') else 'value'
  
  # supers = inspect.getmro(eval('build_onto.' + entry))
  # print(entry, 'emmo-inferred.NominalProperty' in supers, magnetic_material.EnergyDensity in supers, supers, type(supers[0]), supers[1])
  # print(entry, supers)

  # obj = eval('build_onto.' + entry)
  isString = False
  isComplex = False
  if hasattr(obj, 'is_a'):
    attr = getattr(obj, 'is_a')
    print(obj, type(attr[0]), attr)
    if len(attr) > 1:
      print(obj, 'is complex', attr, type(attr[1]), type(attr[1]) is owlready2.class_construct.Restriction)
      for x in attr:
        # Die folgende Zeile koennte den x.type == 24 hack ersetzen. (Der Funktioniert aber eh fuer was wir bisher getestet haben)
        # ACHTUNG: unterscheidung ob magnetic_material oder emmo. Wenn emmo dann gleich wie oben bei Hack
        # type(eval('build_onto.' + str(x.value).split('.')[-1] + '.hasStringValue')) is not NoneType
        if hasattr(x, 'type') and x.type == 24:
          isString = True
      if not isString:
        print(len(attr))
      isComplex = True
      # x = attr[1]
      # namestr = str(x.value)
      # eval('build_onto.' + namestr.split('.')[-1])
  else:
    print(obj, 'has no is_a')
    pass

  unit = getUnit(obj)
  # if unit is not None:
  #   print(obj, unit)
  # else:
  #   print(obj, "has no unit")
  print(f"obj {obj} unit:{unit}, string:{isString}")

  if isComplex:
    ret = generateClassDefComplex(entry, quantName, obj)
  else:
    ret = generateClassDef(entry, quantName, unit, isString)
  # ret = None

  graph.generated.append(entry)

  return ret

def generateMissing(module, depth=0):
  entries = set(list(graph.dependencies.keys()))
  generateMissing2(module, entries)
  print('\nDiff', list(set(list(graph.dependencies.keys())) - entries))
  if list(set(list(graph.dependencies.keys())) - entries) != []:
    print('\n\n\n\n\nStupid recursion', depth)
    generateMissing(module, depth=depth+1)

def generateMissing2(module, entries):
  for entry in entries:
    for depencency in graph.dependencies[entry].dependencies:
      if depencency not in graph.generated:
        print('Generating missing', depencency)
        if depencency.startswith('emmo-inferred.'):
          depencency = depencency[14:]
        elif depencency.startswith('magnetic_material.'):
          depencency = depencency[18:]
        module.body.append(generateForObject(build_onto.emmo.get_by_label(depencency), depencency))

# Load ontology
import build_onto

# Either append the definition to 'nomad_base.py' code
module = ast.parse(open("example_use_case/nomad_generation/nomad_base.py",'r').read())
# module.body.append(k1)


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

  module.body.append(generateForName(entry))

# Or create standalone code
# module = ast.Module(body=[k1],type_ignores=[])


ast.fix_missing_locations(module)
code = compile(module, filename="<ast>", mode="exec")
print(ast.unparse(module))
