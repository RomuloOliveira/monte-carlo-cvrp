Monte Carlo Methods - CVRP
=======================

Python implementation of the Capacitated Vehicle Routing Problem algorithms using Monte Carlo Methods.

Algorithms:

- Clarke and Wright Savings from (CLARKE; WRIGHT, 1964)
- BinaryMCS-CWS algorithm from (TAKES, 2010) (http://www.liacs.nl/~ftakes/pdf/vrp.pdf and http://www.liacs.nl/assets/Masterscripties/2010-01FrankTakes.pdf)
- Monte Carlo Savings (OLIVEIRA, 2014)
  - This is my bachelor's thesis, published article in Portuguese can be found at [2015: Anais Principais do XI Simpósio Brasileiro de Sistemas de Informação](https://sol.sbc.org.br/index.php/sbsi/issue/view/361) ([link to PDF](https://sol.sbc.org.br/index.php/sbsi/article/view/5795/5693))

I use virtualenv to manage packages

### Example usage

```bash
$ python run.py input/Example-k2.vrp 2
```

### Post-publish changes

Original published code can be found at [1.0.0](https://github.com/RomuloOliveira/monte-carlo-cvrp/tree/1.0.0) tag. To see what are the changes added post-publishing follow [this link](https://github.com/RomuloOliveira/monte-carlo-cvrp/compare/1.0.0...master).
