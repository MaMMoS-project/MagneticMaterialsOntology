import ast

# Step 1: Define the nodes for the code you want to generate
# Create a simple function that adds two numbers

# The body of the function
body = [
    ast.Return(
        value=ast.BinOp(left=ast.Name(id='a', ctx=ast.Load()), op=ast.Add(), right=ast.Name(id='b', ctx=ast.Load()))
    )
]

# Create the function definition node
function_def = ast.FunctionDef(
    name='add_numbers',  # Function name
    args=ast.arguments(
        args=[ast.arg(arg='a', annotation=None), ast.arg(arg='b', annotation=None)], 
        vararg=None, posonlyargs=[],kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
    ),
    body=body,
    decorator_list=[],
    returns=None
)

# Step 2: Build a module node with the function definition
module = ast.Module(body=[function_def],type_ignores=[])

# Step 3: Compile the AST into a code object
# first we need to fix missing locations
ast.fix_missing_locations(module)
code = compile(module, filename="<ast>", mode="exec")

# Step 4: Execute the code object
namespace = {}
exec(code, namespace)

# Step 5: Call the dynamically generated function
result = namespace['add_numbers'](5, 7)
# print(f"The result of adding 5 and 7 is: {result}")

# Step 6: Print the source code:
# print(ast.unparse(module))


### and now for something different

# m_def= Section(
#     a_eln=dict(
#       properties=dict(order=[
#         'k1'
#       ])
#     )
#   )
#   k1 = EnergyDensity()

# Assign(
#             targets=[
#                 Name(id='a', ctx=Store()),
#                 Name(id='b', ctx=Store())],
#             value=Constant(value=1))])

# Call(
#         func=Name(id='func', ctx=Load()),
#         args=[
#             Name(id='a', ctx=Load()),
#             Starred(
#                 value=Name(id='d', ctx=Load()),
#                 ctx=Load())],
#         keywords=[
#             keyword(
#                 arg='b',
#                 value=Name(id='c', ctx=Load())),
#             keyword(
#                 value=Name(id='e', ctx=Load()))]))

# @property
# def ontology_label(self) -> str:
#     """
#     str: The ontology label for spontaneous magnetization.
#     """
#     return "SpontaneousMagnetization"

# @property
# def si_units(self) -> set[u.Unit]:
#     """
#     set[astropy.units.Unit]: SI units for spontaneous magnetization, A/m and T.
#     """
#     return {(u.A / u.m), u.T}

ol = ast.FunctionDef(
    name='ontology_label',
    args=ast.arguments(
        args=[ast.arg(arg='self', annotation=None)], 
        vararg=None, posonlyargs=[],kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
    ),
    body=[
        ast.Return(value=ast.Constant(
            value='MagnetocrystallineAnisotropyConstantK1'))
        ],
    decorator_list=[ast.Name(id = 'property', ctx=ast.Load())],
    returns=ast.Name(id='str', ctx=ast.Load()))

si = ast.FunctionDef(
    name='si_units',
    args=ast.arguments(
        args=[ast.arg(arg='self', annotation=None)], 
        vararg=None, posonlyargs=[],kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
    ),
    # return {u.J / u.m}
    body=[
        ast.Return(value=ast.Set(elts=[
            ast.BinOp(left=ast.Attribute(value=ast.Name(id='u', ctx=ast.Load()),
                                         attr='J', ctx=ast.Load()),
                      op=ast.Div(),
                      right=ast.Attribute(value=ast.Name(id='u', ctx=ast.Load()), 
                                          attr='m', ctx=ast.Load()))
            ]))
        ],
    decorator_list=[ast.Name(id = 'property', ctx=ast.Load())],
    returns=ast.Subscript(
                value=ast.Name(id='set', ctx=ast.Load()),
                slice=ast.Attribute(value=ast.Name(id='u', ctx=ast.Load()),
                                    attr='Unit', ctx=ast.Load()),
                ctx=ast.Load())
)

# m_def= Section(a_eln=dict(properties=dict(order=['length'])))

m_defAlt = ast.Assign(
    targets=[ast.Name(id = 'm_def', ctx=ast.Store())],
    # value=ast.Constant(value=1)
    value=ast.Call(func=ast.Name(id='Section', ctx=ast.Load()),
        args=[],
        keywords=[
            ast.keyword(arg='a_eln',
                        value=ast.Constant(value=1))
        ]
    )
)

m_def = ast.Assign(
    targets=[ast.Name(id='m_def', ctx=ast.Store())],
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
                                                                                                       value=ast.List(elts=[
                                                                                                           ast.Constant(value='k1')], ctx=ast.Load()))]))]))]))
value = ast.Assign(
    targets=[ast.Name(id='k1', ctx=ast.Store())],
    value=ast.Call(func=ast.Name(id='EnergyDensity', ctx=ast.Load()), args=[], keywords=[])
    )


k1 = ast.ClassDef(
            name="MagnetocrystallineAnisotropyConstantK1",
            bases=[ast.Name(id="ArchiveSection", ctx=ast.Load())],
            keywords=[],
            # body=[ast.Pass()],
            body=[m_def,value,ol,si],
            decorator_list=[]
)
module = ast.Module(body=[k1],type_ignores=[])
ast.fix_missing_locations(module)
code = compile(module, filename="<ast>", mode="exec")
print(ast.unparse(module))
