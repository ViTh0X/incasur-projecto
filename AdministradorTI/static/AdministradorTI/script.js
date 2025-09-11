const botonInventario_h = document.getElementById('ejecutar_inventario_h');

if (botonInventario_h){
    botonInventario_h.addEventListener('click',function(){
        fetch('/inventario-hardware/iniciar-inventario-hardware/',{
            method:'POST',
            headers:{'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data =>{
            const taskID = data.task_id;
            if(taskID){
                /*Verificacion constante el estado */
                const intervalos = setInterval(()=>{
                    fetch(`/inventario-hardware/status/${taskID}/`)
                    .then(response => response.json())
                    .then(estadoData =>{
                        if(estadoData.estado === 'SUCCESS'){
                            clearInterval(intervalos);
                            // alert("Termino el backup");
                        }
                    })
                },3000);
            }
        });
    });
}

const  botonFaltantes_h = document.getElementById('ejecutar_inventario_faltantes_h');
if(botonFaltantes_h){
    botonFaltantes_h.addEventListener('click',function(){
        fetch('/inventario-hardware/iniciar-faltantes-hardware/',{
            method:'POST',
            headers:{'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data =>{
            const taskID = data.task_id;
            if(taskID){
                /*Verificacion constante el estado */
                const intervalos = setInterval(()=>{
                    fetch(`/inventario-hardware/status/${taskID}/`)
                    .then(response => response.json())
                    .then(estadoData =>{
                        if(estadoData.estado === 'SUCCESS'){
                            clearInterval(intervalos);
                            // alert("Termino el backup");
                        }
                    })
                },3000);
            }
        });
    });
}


const botonInventario_s = document.getElementById('ejecutar_inventario_s');

if (botonInventario_s){
    botonInventario_s.addEventListener('click',function(){
        fetch('/inventario-software/iniciar-inventario-software/',{
            method:'POST',
            headers:{'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data =>{
            const taskID = data.task_id;
            if(taskID){
                /*Verificacion constante el estado */
                const intervalos = setInterval(()=>{
                    fetch(`/inventario-software/status/${taskID}/`)
                    .then(response => response.json())
                    .then(estadoData =>{
                        if(estadoData.estado === 'SUCCESS'){
                            clearInterval(intervalos);
                            // alert("Termino el backup");
                        }
                    })
                },3000);
            }
        });
    });
}

const  botonFaltantes_s = document.getElementById('ejecutar_inventario_faltantes_s');
if(botonFaltantes_s){
    botonFaltantes_s.addEventListener('click',function(){
        fetch('/inventario-software/iniciar-faltantes-software/',{
            method:'POST',
            headers:{'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data =>{
            const taskID = data.task_id;
            if(taskID){
                /*Verificacion constante el estado */
                const intervalos = setInterval(()=>{
                    fetch(`/inventario-software/status/${taskID}/`)
                    .then(response => response.json())
                    .then(estadoData =>{
                        if(estadoData.estado === 'SUCCESS'){
                            clearInterval(intervalos);
                            // alert("Termino el backup");
                        }
                    })
                },3000);
            }
        });
    });
}


const boton_backup = document.getElementById('ejecutar_backup');

if (boton_backup){
    boton_backup.addEventListener('click',function(){
        fetch('/backup-informacion/iniciar-backup-informacion/',{
            method:'POST',
            headers:{'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data =>{
            const taskID = data.task_id;
            if(taskID){
                /*Verificacion constante el estado */
                const intervalos = setInterval(()=>{
                    fetch(`/backup-informacion/status/${taskID}/`)
                    .then(response => response.json())
                    .then(estadoData =>{
                        if(estadoData.estado === 'SUCCESS'){
                            clearInterval(intervalos);
                            // alert("Termino el backup");
                        }
                    })
                },3000);
            }
        });
    });
}

const boton_backup_faltantes = document.getElementById('ejecutar_backup_faltantes');
if(boton_backup_faltantes){
    boton_backup_faltantes.addEventListener('click',function(){
        fetch('/backup-informacion/iniciar-faltantes-backup/',{
            method:'POST',
            headers:{'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data =>{
            const taskID = data.task_id;
            if(taskID){
                /*Verificacion constante el estado */
                const intervalos = setInterval(()=>{
                    fetch(`/backup-informacion/status/${taskID}/`)
                    .then(response => response.json())
                    .then(estadoData =>{
                        if(estadoData.estado === 'SUCCESS'){
                            clearInterval(intervalos);
                            // alert("Termino el backup");
                        }
                    })
                },3000);
            }
        });
    });
}
