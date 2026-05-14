# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# Configuration Reference:  https://reframe-hpc.readthedocs.io/en/stable/config_reference.html?highlight=logging#configuration-reference
#
# SPDX-License-Identifier: BSD-3-Clause
#
# Yoltla settings
#
# rfmdocstart: site-configuration
site_configuration = {
    # Una lista de objetos de configuración del sistema.
    # https://reframe-hpc.readthedocs.io/en/stable/config_reference.html?highlight=logging#system-configuration
    'systems': [
        {
            # El nombre del sistema, se utiliza para referirse a este sistema en otros contextos
            'name': 'yoltla',
            # Descripción
            'descr': 'settings para el cluster yoltla',
            # ReFrame obtiene el nombre de la maquina con /etc/xthostname o el comando hostname
            # y selecciona la configuración de ese sistema.
            'hostnames': ['yoltla.supercomputo.izt.uam.mx','nc','tt'],
            # implementación de Tcl de los módulos de entorno (versión 3.2).
            'modules_system': 'tmod32', 
            # Una lista de objetos de configuración de la partición del sistema. Esta lista debe tener al menos un elemento.
            #https://reframe-hpc.readthedocs.io/en/stable/config_reference.html?highlight=logging#system-partition-configuration       
            'partitions': [
            	# Nodos nc
                {
                    # Nombre de la partición
                    'name': 'q1h-20p',
                    # El gestor de carga de trabajo (planificador de trabajos) 
                    # que se utiliza en esta partición para lanzar trabajos paralelos
                    'scheduler': 'slurm',
                    # Recursos de la particion
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1h-20p'],
                    # Lista de entornos que utilizará ReFrame para ejecutar pruebas de regresión en esta partición
                    # Nombres simbólicos que se refieren a entornos definidos en la sección environments
                    'environs': ['defecto','builtin-gcc-7.2.0'],
                    'descr': 'particion q1h-20p', 
                    # Los programas paralelos se lanzarán usando el comando srun de Slurm
                    'launcher': 'srun'
                },
                {
                    # Nombre de la partición
                    'name': 'q1d-20p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1d-20p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'],
                    'descr': 'particion q1d-20p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q4d-20p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q4d-20p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'],
                    'descr': 'particion q4d-20p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q7d-20p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q7d-20p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q7d-20p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q1h-40p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1h-40p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q1h-40p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q1d-40p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1d-40p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q1d-40p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q4d-40p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q4d-40p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q4d-40p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q1h-80p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1h-80p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q1h-80p', 
                    'launcher': 'srun' 
                },      
                {
                    # Nombre de la partición
                    'name': 'q12h-80p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q12h-80p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q12h-80p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q1d-80p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1d-80p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q1d-80p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q4d-80p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q4d-80p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q4d-80p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q1h-160p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1h-160p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q1h-160p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q12h-160p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q12h-160p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q12h-160p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q1d-160p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1d-160p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q1d-160p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q1h-320p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1h-320p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q1h-320p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q12h-320p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q12h-320p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q12h-320p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'q1d-320p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=q1d-320p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion q1d-320p', 
                    'launcher': 'srun' 
                },
                # Nodos tt
                {
                    # Nombre de la partición
                    'name': 'tt2d-80p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt2d-80p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion tt2d-80p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'tt2d-100p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt2d-100p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion tt2d-100p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'tt1d-160p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt1d-160p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion tt1d-160p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'tt12h-320p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt12h-320p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion tt12h-320p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'tt2d-64p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt2d-64p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion tt2d-64p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'tt1d-128p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt1d-128p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion tt1d-128p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'tt1d-256p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt1d-256p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion tt1d-256p', 
                    'launcher': 'srun' 
                },  
                {
                    # Nombre de la partición
                    'name': 'tt1d-512p',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=tt1d-512p'],
                    'environs': ['defecto','builtin-gcc-7.2.0'],
                    'descr': 'particion tt1d-512p', 
                    'launcher': 'srun' 
                },
                {
                    # Nombre de la partición
                    'name': 'gpus',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=gpus'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion gpus', 
                    'launcher': 'srun' 
                },  
                {
                    # Nombre de la partición
                    'name': 'vgpus',
                    'scheduler': 'slurm',
                    'resources':[],
                    'modules': [],
                    'access': ['--partition=vgpus'],
                    'environs': ['defecto','builtin-gcc-7.2.0'], 
                    'descr': 'particion vgpus', 
                    'launcher': 'srun' 
                }                                    
            ]
        }
    ],
    # Los entornos definidos en esta sección se utilizarán para ejecutar pruebas de regresión. Están asociados con particiones del sistema.
    # https://reframe-hpc.readthedocs.io/en/stable/config_reference.html?highlight=logging#environment-configuration
    'environments': [
        {
            'name': 'defecto',
            'modules': [],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
        {
            'name': 'builtin-gcc-7.2.0',
            'modules': ['gcc/7.2.0'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        }
    ],
    # Seccion que controla los mensajes log
    # ver: https://reframe-hpc.readthedocs.io/en/stable/config_reference.html?highlight=logging#logging-configuration
    'logging': [
        { 
            # El nivel asociado con objetos log.
            'level': 'debug', # Mensajes debug.
            # Una lista de controladores de mensajes log responsables de manejar la salida normal.
            # https://reframe-hpc.readthedocs.io/en/stable/config_reference.html?highlight=logging#logging-.handlers
            'handlers': [
                {
                    'type': 'stream',                   # Este controlador envía mensajes log a un archivo stream
                    'name': 'stdout',                   # la salida estándar.
                    'level': 'info',                    # Mensajes informativos.
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   
                    'append': False
                }
            ],
            # Una lista de controladores de registro responsables de manejar los datos de rendimiento de las pruebas.
            # https://reframe-hpc.readthedocs.io/en/stable/config_reference.html?highlight=logging#logging-.handlers_perflog
            'handlers_perflog': [
                {
                    'type': 'filelog', # Este controlador envía registros log de rendimiento a archivos.
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',   # Mensajes informativos.
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True     # Controla si este controlador debe agregarse a su archivo o no.
                }       
            ]
        }
    ],
    'general': [
        {
            #'remote_workdir': '/LUSTRE/home/uam/izt/lsvp/..', # Directorio de trabajo temporal para copias de reframe 
            'remote_detect': True,                      # Para detectar topologia (tiene conflicto con use_nodes_option)
            'purge_environment': True,                  # Purga los módulos de entorno cargados antes de ejecutar cualquier prueba
            #'report_file': 'logs/run-report.json',      # Archivo donde ReFrame almacenará su informe
            #'timestamp_dirs': '%d-%m-%Y/%H-%M-%S'       # Agrega una marca de tiempo a los prefijos de los directorios stage/output
        }
    ],
    'schedulers': [
        {
            'name': 'slurm',
            'ignore_reqnodenotavail': True,             # Evita que se cancelen los trabajos cuando no hay nodos disponibles
            #'use_nodes_option': True                    # Siempre agrega la directiva --nodes a los scripts de Slurm 
        }
    ]
    # rfmdocend: logging
} # Fin site_configuration
# rfmdocend: site-configuration