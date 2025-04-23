from astropy import units as u
import owlready2
from ontopy import ontology
import owlready2.entity
import re
import traceback
import copy

def auto_str(cls):
  def __str__(self):
    return '%s(%s)' % (
        type(self).__name__,
        ', '.join('%s=%s' % item for item in vars(self).items())
    )
  cls.__str__ = __str__
  def __repr__(self):
    return self.__str__()
  cls.__repr__ = __repr__
  return cls

# @auto_str
# class Component:
#     def __init__(self, unit, label):
#         self.unit = unit
#         self.label = label

@auto_str
class OntoObject:
    def __init__(self, name):
        self.name = name
        self.unit = None
        self.label = None
        self.parents = []
        self.components = []
        self.repeats = False

def convert_to_iso_unit(unit_string):
    """Converts a string representation of ISQ base quantities to its ISO unit symbols using astropy.

    Args:
        unit_string: The string representation of the ISQ base quantities.

    Returns:
        The ISO unit symbols as astropy object.
    """

    # print(unit_string, unit_string == 'T0 L0 M0 I0 Θ0 N0 J0')
    # if unit_string == 'T0 L0 M0 I0 Θ0 N0 J0':
    #     return u.Unit('1')

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
    print(f"Converting to unit '{unit_string} -> '{astropy_unit}'")
    return u.Unit(astropy_unit)



def getUnit(entity):
    # print(entity, 'getUnit')
    class_prop = entity.get_class_properties()
    if any([str(prop).endswith('hasMeasurementUnit') for prop in class_prop]):
        print(f'Measurement unit property found for class {entity} : {entity.hasMeasurementUnit[0]}')
        try:
            return u.Unit(entity.hasMeasurementUnit[0].ucumCode[0])
        except Exception as e:
            print(f'Error: {e}')
            traceback.print_stack()
            return None

def parseObject(object):
    ret = OntoObject(str(object))
    if hasattr(object, '__prefLabel'):
        ret.label = object.__prefLabel[0][:]

    ret.unit = getUnit(object)

    # Parse components / is_a
    attr = getattr(object, 'is_a')

    print(object, [str(a) for a in attr])
    attr = [a for a in attr if str(a).replace('emmo-inferred', 'emmo') != str(object)]

    for component in attr:
        whiteList = [
        # entry is a restriction , and
        type(component) is owlready2.class_construct.Restriction and (
            # either a dimension string i.e. it tells us which unit it is
            str(component.property).find('hasDimensionString') != -1 or
            str(component.property).find('hasMeasurementUnit') != -1 or 
            str(component.property).find('hasMetrologicalReference') != -1 or 
            str(component.property).find('hasProperty') != -1
            ),
        type(component) is owlready2.entity.ThingClass
        ]

        if not any(whiteList):
            print(component, 'is not white listed')
            continue

        if type(component) is owlready2.class_construct.Restriction:
            print(component, 'is restriction')

            strProp = str(component.property).replace('emmo-inferred.','').replace('emmo.', '')
            typeString = str(component).split('.')[-1]
            print(f'Parsing restriction {strProp} typeT {typeString} classes {hasattr(component.value,"Classes")}')
            if strProp == 'hasDimensionString':
                unit = convert_to_iso_unit(typeString)
                print(object, 'converted to unit', unit, unit.to_string('vounit', fraction=True))

                if ret.unit is not None:
                    raise Exception('Cannot have two units')
                ret.unit = unit
            elif strProp == 'hasMetrologicalReference':
                reference = component.value
                if hasattr(reference, 'hasDimensionString'):
                    dimStr = reference.hasDimensionString
                    if dimStr is not None:
                        print(reference.hasDimensionString)
                        unit = convert_to_iso_unit(reference.hasDimensionString)
                        print(object, 'converted to unit', unit, unit.to_string('vounit', fraction=True) if unit is not None else '')

                        if ret.unit is not None:
                            raise Exception('Cannot have two units')
                        ret.unit = unit
                    else:
                        print('dimensionString was none')
                else:
                    print(object, component, 'has no unit')
            elif strProp == 'hasMeasurementUnit':
                measurementUnit = parseObject(component.value)
                if not canReduce(measurementUnit):
                    raise Exception('Cannot reduce measurement unit')
                else:
                    reducedMeasurementUnit = reduce(measurementUnit)
                    if ret.unit is not None:
                        # if ret.unit.to_string('vounit', fraction=True) != reducedMeasurementUnit.unit.to_string('vounit', fraction=True):
                        if not u.allclose(ret.unit * 3.1415, reducedMeasurementUnit.unit * 3.1415):
                            print(ret.unit.to_string('vounit', fraction=True))
                            print(reducedMeasurementUnit.unit.to_string('vounit', fraction=True))
                            raise Exception(ret.name + ' cannot have two different units')
                    ret.unit = reducedMeasurementUnit.unit
            elif strProp == 'hasProperty':
                # raise Exception('hasProperty not implemented')
            

                # Now we need to check if this is a hasProperty.TYPE restriction
                #  if it is hasProperty.min, then type == 27. We need to have this option to treat min(0,....) as repeats=True
                repeats = True if hasattr(component, 'cardinality') and component.cardinality is not None and (component.cardinality > 1 or component.get_typename() == 'min') else False

                # Check if this restriction is a restriction to a single class or to multiple classes
                # if it does not have classes, it is to a single class.
                # if it has classes, it is to multiple classes. --> In Nomad we cannot do this, so we create a SubSection for each class
                if not hasattr(component.value, 'Classes'):
                    subobj = parseObject(component.value)
                    subobj.repeats = repeats
                    ret.components.append(subobj)
                else:
                    for alternative in component.value.Classes:
                        # print('y', alternative)
                        # typeT = str(alternative).split('.')[-1]
                        # subobj = parseObject(typeT)
                        subobj = parseObject(alternative)
                        subobj.repeats = repeats
                        ret.components.append(subobj)

        elif type(component) is owlready2.entity.ThingClass:
            print(component, 'is parent')
            parent = str(component)
            parent = parent.replace('emmo-inferred', 'emmo')
            if parent != 'owl.Thing': # Check if we hit the top of tree
              # alternative if parent != 'emmo.EMMO'
              ret.parents.append(parseObject(component)) # TODO: what about emmo-inferred?

    print(ret)
    return ret

def canReduce(object: OntoObject) -> bool:
    if object.parents == [] and object.components == []:
        return True
    elif object.parents == [] and object.components != []:
        # Object has components -> cannot be reduced
        return False
    elif object.parents != [] and object.components == []:
        return all([canReduce(p) for p in object.parents])
    else:
        print(object.name, len(object.components), len(object.parents))
        # Object has components and parents
        return all([canReduce(p) for p in object.parents]) # and all([canReduce(c) for c in object.components])
        raise Exception('Wait what?')
    
def reduce(object: OntoObject) -> OntoObject:
    if not canReduce(object):
        raise Exception('Cannot reduce object') #TODO better type for exception
    
    if object.parents == [] and object.components == []:
        return object
    
    # we either have components in this object or need to check if we have some information from parents

    ret = copy.deepcopy(object)
    components = []
    if len(object.parents) == 1:
        parent = reduce(object.parents[0])
        ret = copy.deepcopy(object)
        if parent.unit is not None:
            if object.unit is not None:
                raise Exception('Cannot have two units')
            ret.unit = parent.unit

        ret.parents = []
        components.extend(parent.components)    
    elif len(object.parents) > 1:
        print(object.label, 'has multiple parents', object.parents)
        parents = [reduce(parent) for parent in object.parents]
        for parent in parents:
            if parent.unit is not None:
                if object.unit is not None:
                    raise Exception('Cannot have two units')
                ret.unit = parent.unit
            components.extend(parent.components)
        ret.parents = []

    components.extend([reduce(component) for component in object.components])

    ret.components = components
    return ret

if __name__ == "__main__":
    # # Load the local stored ontology file
    emmo = ontology.get_ontology('./magnetic_material_mammos.ttl')
    emmo.load()

    print('Start')
    # obj = emmo.get_by_label('LatticeConstantAlpha')
    # # print(obj, type(obj))
    # parseObject(obj)

    # print('')

    # obj = eval('build_onto.EnergyDensity')
    # print(obj, type(obj))
    # parseObject(obj)

    obj = eval('build_onto.LatticeConstantAlpha')
    # print(obj, type(obj))
    parseObject(obj)


    # obj = eval('build_onto.SampleGeometry')
    # print(obj, type(obj))
    # parseObject(obj)
