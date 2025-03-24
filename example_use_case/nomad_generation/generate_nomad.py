import ast

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

  # Create an instance of the object from the onotolgy
  obj = eval(f'build_onto.{entry}')
  quantName = obj.get_preferred_label()[:] if hasattr(obj,'altLabel') else 'value'
  
  module.body.append(generateClassDef(entry, quantName, 'EnergyDensity'))
  # print(entry, supers)

# Or create standalone code
# module = ast.Module(body=[k1],type_ignores=[])


ast.fix_missing_locations(module)
code = compile(module, filename="<ast>", mode="exec")
print(ast.unparse(module))
