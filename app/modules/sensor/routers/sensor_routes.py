from fastapi import APIRouter, Depends, Security, status, Response
from ..schemas.sensor_schema import CreateSensorInSchema, SensorOutSchema, UpdateSensorInSchema, SensorConfigOutSchema, ListenerConfigInSchema, ListenerConfigOutSchema
from ..controllers.sensor_listener_controller import sensor_listener_controller
from ..controllers.sensor_config_controller import sensor_config_controller

router = APIRouter(
    prefix='/sensor',
    tags=['Sensor']
)


@router.post('/configure',  status_code=status.HTTP_201_CREATED, response_model=SensorConfigOutSchema)
async def create_new_sensor_config(new_sensor_config: CreateSensorInSchema):    
    return sensor_config_controller.create_new_sensor_config(new_sensor_config)


@router.put('/configure/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=SensorConfigOutSchema)
async def update_sensor_config(id: int, updated_sensor_config: UpdateSensorInSchema):   
    return sensor_config_controller.update_sensor_config(id, updated_sensor_config)


@router.delete('/delete_config/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_sensor_config(id: int):
    sensor_config_controller.delete_sensor_config(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/config/get/{id}', status_code=200, response_model=SensorConfigOutSchema)
async def get_sensor_config(id: int):   
    return sensor_config_controller.get_sensor_config(id)


@router.put('/configure_listener', response_model=ListenerConfigOutSchema, status_code=status.HTTP_202_ACCEPTED)
async def configure_listener(listener_config: ListenerConfigInSchema):
    status: int = sensor_listener_controller.manage_listener(listener_config)
    if status == 0:
        return {
            "state": "Success",
            "msgs": ["Listener state updated successfully"]
        }
    elif status == 1:
        return {
            "state": "Error",
            "msgs": ["Start listener failed"]
        }
    else:
        return {
            "state": "Error",
            "msgs": ["Shuttingdown listener failed"]
        }

# Create an endpoint to get the listener state
# ...
    
