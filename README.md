# tokentranslator
Experimental project. Can be used to create equations or proposals translators by defining replacers for each term (token) with use of gui web interface. Currently contain support for Wolfram->sympy (or cpp), Tex-> sympy (or cpp).
Also can extract arguments from equation/proposal. Has experimental sampling proposal generator i.e. for proposal can create subset of it's arguments at which this proposal is true.

### Examples of translation:
#### Tex to sympy (cpp):
```
   U'=a*(\\frac{d^2U}{dx^2}+ \\frac{d^2U}{dy^2})

translated to:
   (sympy)
     sympy.diff(U(t), t)=a*(diff(U,x, 2)+diff(U,y, 2))

   (cpp)
     result[idx + 0]=params[0]*((DXM2 * (source[0][idx + 1 * Block0StrideX * Block0CELLSIZE + 0] - 2.0 * source[0][idx + 0 * Block0StrideX * Block0CELLSIZE + 0] + source[0][idx-1 * Block0StrideX * Block0CELLSIZE + 0]))+(DYM2 * (source[0][idx + 1 * Block0StrideY * Block0CELLSIZE + 0] - 2.0 * source[0][idx + 0 * Block0StrideY * Block0CELLSIZE + 0] + source[0][idx-1 * Block0StrideY * Block0CELLSIZE + 0])))

U'=a*(\\frac{d^2U}{dx^2}+ \\frac{d^2U}{dy^2})+sin(x)+A.transpose().conj()

translated to
   (sympy)
      sympy.diff(U(t), t)=a*(diff(U,x, 2)+diff(U,y, 2))+sympy.sin(x)+A.transpose().conj()

   (cpp)
      result[idx + 0]=params[0]*((DXM2 * (source[0][idx + 1 * Block0StrideX * Block0CELLSIZE + 0] - 2.0 * source[0][idx + 0 * Block0StrideX * Block0CELLSIZE + 0] + source[0][idx-1 * Block0StrideX * Block0CELLSIZE + 0]))+(DYM2 * (source[0][idx + 1 * Block0StrideY * Block0CELLSIZE + 0] - 2.0 * source[0][idx + 0 * Block0StrideY * Block0CELLSIZE + 0] + source[0][idx-1 * Block0StrideY * Block0CELLSIZE + 0])))+sin((Block0OffsetX+idxX*DX))+A.transpose().conj()
```
### requirements
```
linux, python3

```
### installation and running
```
source ~/anaconda3/bin/./activate parser_env 
~/anaconda3/envs/parser_env/bin/./pip install tokentranslator


# for web interface:
~/anaconda3/envs/parser_env/bin/./python3 -c "import tokentranslator.gui.web.server.server_main as sm; sm.run()"

```

### usage
##### parsing equations (defalut from Wolfram)
```
from tokentranslator.db_models.model_main import TokenizerDB
from tokentranslator.env.equation_net.equation import Equation

model = TokenizerDB()

eq = Equation("U'=a*(D[U,{x, 2}]+D[U,{y,2}])", db=model)
eq.parser.parse()

# set default params (like dimension, bounds type (Dirichlet or Neumann) an so on):
eq.replacer.cpp.editor.set_default()
eq.replacer.cpp.make_cpp()

print('\noriginal:')
eq.show_original()

print("\nparsed tree:")
eq.show_cyk_out()
        
print('\ncpp:')
eq.replacer.cpp.show_cpp()

print("\nsympy:")
eq.replacer.sympy.make_sympy()
eq.replacer.sympy.show_sympy()

```
##### parsing equations (from TeX)
```
# there is currently two dialect databases for equations:
# 'env/equation_net/data/terms/input/tex_dialect.db' for tex
# 'env/equation_net/data/terms/input/demo_dialect.db' for wolfram
# default is wolfram

# to change to tex use commands:
model.save_path("eqs", "env/equation_net/data/terms/input/tex_dialect.db")
model.change_dialect_db("eqs")
# this change "eqs" path for all parsers wherever they run.
# show current dialect.db path:
model.get_path_of_dialect_db("eqs")

# if it's ended with tex_dialect.db then tex input used
# remained is same as above:

eq = Equation("U'=a*(\\frac{d^2U}{dx^2}+ \\frac{d^2U}{dy^2})", db=model)
eq.parser.show_patterns()
eq.parser.parse()

print('\noriginal:')
eq.show_original()

print("\nparsed tree:")
eq.show_cyk_out()
        
print('\ncpp:')
eq.replacer.cpp.show_cpp()

print("\nsympy:")
eq.replacer.sympy.make_sympy()
eq.replacer.sympy.show_sympy()

# find vars:
from proposalsampler.sampling.vars.vars_extractor import Extractor
import proposalsampler.sampling.vars.vars_maps as vms
vars_extractor = Extractor("eqs")                                      
net_vars = vms.get_args(str(["s"]), clause.net_out.copy(), vars_extractor)
print(net_vars)
```
##### parsing proposals:
```
from tokentranslator.db_models.model_main import TokenizerDB
from tokentranslator.env.clause.clause_main import Clause

model = TokenizerDB()

# switch to clauses db:
model.change_dialect_db("cs")

clause = Clause("bilinear(f)=>Eq(f(x,y,)=g(x,y,)+h(x,y,))Eq"
		+ "\\where (g: simmetric(g)) \\and (h: simplectic(h))", db=model)
clause.parser.parse()

# there is currently no dialect to translate clause to, so just check it's generated tree:
clause.show_cyk_out()
# this tree will be used for proposal sampling.

# !for equation parser to work don't forget change db back:
model.change_dialect_db("eqs")
# even if You in other session! 

# find vars:
from tokentranslator.translator.sampling.vars.vars_extractor import Extractor
import tokentranslator.translator.sampling.vars.vars_maps as vms
vars_extractor = Extractor("cs")                                      
net_vars = vms.get_args(str(["s"]), clause.net_out.copy(), vars_extractor)
print(net_vars)
```
### References:

##### Parser:
Cocke–Younger–Kasami algorithm: https://en.wikipedia.org/wiki/CYK_algorithm

### Acknowledgments:
##### Used software:
networkx: https://networkx.github.io/ <br/>
cytoscape: https://js.cytoscape.org/ <br/>
fancytree: https://github.com/mar10/fancytree <br/>
codemirror: https://codemirror.net/ <br/>
tabulator: https://github.com/olifolkerd/tabulator <br/>


