# Instalar aplicaciones


## Descripción

En este documentos se describen diversas formas de realizar instalaciones en el 
clúster Yoltla.


## Spack y scope

Este método permite realizar instalaciones con dependencias completamente separadas de 
la instancia principal de spack.
Como inconveniente se tiene la redundancia de dependencias, pero se gana claridad y 
se resta complejidad.

En el Home de la cuenta spack se debe crear el directorio que albergará  la instalación 
junto con sus dependencias.

dentro de este directorio se debe crear el directorio 'spack_scope'. e.g.

```bash
/LUSTRE/yoltla/programas/elk/7.2.42/spack_scope
```

y dentro del directorio el archivo 'config.yaml' donde se especifican los directorios
de instalación y compilación. e.g.

```bash
config:
  install_tree:
    root: /LUSTRE/yoltla/programas/elk/7.2.42/deps
  module_roots:
    tcl: /LUSTRE/yoltla/programas/elk/7.2.42/module
    lmod: /LUSTRE/yoltla/programas/elk/7.2.42/lmod
  build_stage: /LUSTRE/yoltla/programas/elk/7.2.42/stage
```

Para utilizar el  scope se debe usar el comando de spack -C. e.g.

```bash
spack -C /LUSTRE/yoltla/programas/elk/7.2.42/spack_scope
```

Recomiendo agregarlo a un alias. e.g

```bash
alias spack='spack -C /LUSTRE/yoltla/programas/elk/7.2.42/spack_scope'
```

A partir de aquí se pueden usar comando de spack sin ninguna diferencia al modo de 
trabajo regular.
