import ast
import inspect
import re
from astropy import units as u

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

def generateQuantityStatement(name,type):
  return ast.Assign(
    targets=[ast.Name(id=name, ctx=ast.Store())],
    value=ast.Call(func=ast.Name(id=type, ctx=ast.Load()), args=[], keywords=[])
    )


def generateClassDef(name,attrname,type):
  return ast.ClassDef(
            name=name,
            bases=[ast.Name(id="ArchiveSection", ctx=ast.Load())],
            keywords=[],
            body=[
              generateMDef([attrname]),
              generateQuantityStatement(attrname,type)],
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
    units = re.findall(r'([TLMIΘNJ])([+-]?\d+)', unit_string)

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
  print(class_prop)
  if build_onto.emmo.hasMeasurementUnit in list(class_prop):
    print('Measurement unit property found for class ')
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




def generateForName(entry):
  # Create an instance of the object from the onotolgy
  obj = eval(f'build_onto.{entry}')
  quantName = obj.get_preferred_label()[:] if hasattr(obj,'altLabel') else 'value'
  
  ret = generateClassDef(entry, quantName, 'EnergyDensity')
  supers = inspect.getmro(eval('build_onto.' + entry))
  # print(entry, 'emmo-inferred.NominalProperty' in supers, magnetic_material.EnergyDensity in supers, supers, type(supers[0]), supers[1])
  # print(entry, supers)

  obj = eval('build_onto.' + entry)
  if hasattr(obj, 'is_a'):
    attr = getattr(obj, 'is_a')
    # print(obj, type(attr[0]), attr)
    if len(attr) > 1:
      print(obj, 'is complex')
  else:
    # print(obj, 'has no is_a')
    pass

  unit = getUnit(obj)
  if unit is not None:
    print(obj, unit)
  else:
    print(obj, "has no unit")

  return ret


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

  module.body.append(generateForName(entry))

# Or create standalone code
# module = ast.Module(body=[k1],type_ignores=[])


ast.fix_missing_locations(module)
code = compile(module, filename="<ast>", mode="exec")
print(ast.unparse(module))
