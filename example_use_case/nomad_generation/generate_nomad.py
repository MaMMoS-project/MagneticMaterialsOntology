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


k1 = ast.ClassDef(
            name="MagnetocrystallineAnisotropyConstantK1",
            bases=[ast.Name(id="ArchiveSection", ctx=ast.Load())],
            keywords=[],
            body=[
              generateMDef(['k1']),
              generateQuantityStatement('k1','EnergyDensity')],
            decorator_list=[]
)


# Either append the definition to 'nomad_base.py' code
module = ast.parse(open("example_use_case/nomad_generation/nomad_base.py",'r').read())
module.body.append(k1)

# Or create standalone code
# module = ast.Module(body=[k1],type_ignores=[])



ast.fix_missing_locations(module)
code = compile(module, filename="<ast>", mode="exec")
print(ast.unparse(module))
