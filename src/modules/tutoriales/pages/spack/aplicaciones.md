# HPL

## Descripción

HPL es un paquete de software que resuelve un sistema lineal denso (aleatorio) en aritmética 
de doble precisión (64 bits) en computadoras con memoria distribuida. Por lo tanto, se puede 
considerar como una implementación portátil y de libre acceso del High Performance Computing 
Linpack Benchmark.

Para obtener más información, visite el sitio oficial de [HPL](https://netlib.org/benchmark/hpl/).


## Instalación

Para instalar HPL, ejecute el comando:

```bash
[t.800@yoltla ~]$ spack install hpl
==> intel-mkl@2017.4.239 : has external module in ['intel/mkl-2017u4']
[+] /LUSTRE/yoltla/compiladores/intel/parallel_studio_xe_2017_update4/compilers_and_libraries_2017.4.196/linux/mkl/lib/intel64 (external intel-mkl-2017.4.239-qkzp6oh4caiy7vm2hen7a5xnndxpd6br)
==> intel-mpi@2017.0.4 : has external module in ['intel/impi-2017u4']
[+] /LUSTRE/yoltla/compiladores/intel/parallel_studio_xe_2017_update4/compilers_and_libraries_2017.4.196/linux/mpi/intel64 (external intel-mpi-2017.0.4-eb7655s35tmvobbjzlnys66eiqn6wvhn)
==> Installing hpl-2.3-sagktyb3xjpdemwaqmyal44uy36kdxks
==> No binary for hpl-2.3-sagktyb3xjpdemwaqmyal44uy36kdxks found: installing from source
==> Using cached archive: /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack/var/spack/cache/_source-cache/archive/32/32c5c17d22330e6f2337b681aded51637fb6008d3f0eb7c277b163fadd612830.tar.gz
==> No patches needed for hpl
==> hpl: Executing phase: 'autoreconf'
==> hpl: Executing phase: 'configure'
==> hpl: Executing phase: 'build'
==> hpl: Executing phase: 'install'
==> hpl: Successfully installed hpl-2.3-sagktyb3xjpdemwaqmyal44uy36kdxks
  Fetch: 0.04s.  Build: 55.92s.  Total: 55.97s.
[+] /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/hpl-2.3-sagktyb3xjpdemwaqmyal44uy36kdxks
```

Puede verificar la instalación de HPL utilizando el comando:

```bash
[t.800@yoltla ~]$ spack find hpl
==> 1 installed package
-- linux-centos6-ivybridge / gcc@7.2.0 --------------------------
hpl@2.3
```


# HPCG


## Descripción

El proyecto High Performance Conjugate Gradients (HPCG) es un esfuerzo por crear una 
nueva métrica para clasificar los sistemas HPC. HPCG está pensado como un complemento 
al benchmark High Performance LINPACK (HPL).

Para obtener más información, visite el sitio oficial de [HPCG](https://hpcg.info/).


## Instalación

Para instalar HPCG, ejecute el comando:

```bash
[t.800@yoltla ~]$ spack install hpcg
==> intel-mpi@2017.0.4 : has external module in ['intel/impi-2017u4']
[+] /LUSTRE/yoltla/compiladores/intel/parallel_studio_xe_2017_update4/compilers_and_libraries_2017.4.196/linux/mpi/intel64 (external intel-mpi-2017.0.4-eb7655s35tmvobbjzlnys66eiqn6wvhn)
==> Installing hpcg-3.1-22yol5x2gdcaqb5fjcak5vccpazffcd2
==> No binary for hpcg-3.1-22yol5x2gdcaqb5fjcak5vccpazffcd2 found: installing from source
==> Fetching https://mirror.spack.io/_source-cache/archive/33/33a434e716b79e59e745f77ff72639c32623e7f928eeb7977655ffcaade0f4a4.tar.gz
==> No patches needed for hpcg
==> hpcg: Executing phase: 'autoreconf'
==> hpcg: Executing phase: 'configure'
==> hpcg: Executing phase: 'build'
==> hpcg: Executing phase: 'install'
==> hpcg: Successfully installed hpcg-3.1-22yol5x2gdcaqb5fjcak5vccpazffcd2
  Fetch: 0.98s.  Build: 4.73s.  Total: 5.71s.
[+] /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/hpcg-3.1-22yol5x2gdcaqb5fjcak5vccpazffcd2
```

Puede verificar la instalación de HPCG utilizando el comando:

```bash
[t.800@yoltla ~]$ spack find hpcg
==> 1 installed package
-- linux-centos6-ivybridge / gcc@7.2.0 --------------------------
hpcg@3.1
```


# memtester


## Descripción

memtester es una utilidad para probar el subsistema de memoria en una computadora para 
determinar si está defectuoso.

Para obtener más información, visite el sitio oficial de [memtester](https://pyropus.ca./software/memtester/).


## Instalación

Para instalar memtester, ejecute el comando:

```bash
[t.800@yoltla ~]$ spack install memtester
==> Installing memtester-4.3.0-mttqeqxf5zlzqoooooyooavqzn54tzbk
==> No binary for memtester-4.3.0-mttqeqxf5zlzqoooooyooavqzn54tzbk found: installing from source
==> Fetching https://mirror.spack.io/_source-cache/archive/f9/f9dfe2fd737c38fad6535bbab327da9a21f7ce4ea6f18c7b3339adef6bf5fd88.tar.gz
==> No patches needed for memtester
==> memtester: Executing phase: 'edit'
==> memtester: Executing phase: 'build'
==> memtester: Executing phase: 'install'
==> memtester: Successfully installed memtester-4.3.0-mttqeqxf5zlzqoooooyooavqzn54tzbk
  Fetch: 0.63s.  Build: 2.87s.  Total: 3.50s.
  [+] /LUSTRE/home/uam/izt/lsvp/edra/colaboradores/t.800/spack_scope/deps/linux-centos6-ivybridge/gcc-7.2.0/memtester-4.3.0-mttqeqxf5zlzqoooooyooavqzn54tzbk
```

Puede verificar la instalación de memtester utilizando el comando:

```bash
[t.800@yoltla ~]$ spack find memtester
==> 1 installed package
-- linux-centos6-ivybridge / gcc@7.2.0 --------------------------
memtester@4.3.0
```
