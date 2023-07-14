from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

app = FastAPI()


class Cuenta(BaseModel):
    minumero:str
    name:str
    monto:int 
    numerosDestino:list[str]

class Operacion(BaseModel):
    minumero:str
    numeroDestino:str
    fecha:str
    valor:int

#creo lista para cuentas 
DB = [
    Cuenta(minumero="21345", name="Arnaldo", monto=200, numerosDestino=["123", "456"]),
    Cuenta(minumero="123", name="Luisa", monto=400, numerosDestino=["456"]),
    Cuenta(minumero="456", name="Andrea", monto=300, numerosDestino=["21345"])
]
BD_Operaciones=[Operacion(minumero="21345", numeroDestino="123", fecha="01/01/2021", valor=100)]


# Lista de mensajes
#DB_MENSAJES= [Mensaje(alias_origen="cpaz", alias_destino="lmunoz", fecha="01/01/2021", texto="Hola Luisa"),Mensaje(alias_origen="lmunoz", alias_destino="mgrau", fecha="01/01/2021", texto="Hola Miguel"),Mensaje(alias_origen="mgrau", alias_destino="cpaz", fecha="01/01/2021", texto="Hola Christian")]

def getCuenta(name: str) -> Cuenta|None:
    for u in DB:
        if u.name == name:
            return u
   # return None

@app.get("/billetera/contactos")
def gente_pagar( minumero: str | None = None):
    temp_contactos = []
    res = []
    if minumero is None:
        return {"contactos": []}
    else:
        for u in DB:
            #print(temp_contactos)
            #print(res)
            if u.minumero == minumero:
                temp_contactos = u.numerosDestino
            if u.minumero in temp_contactos:
                res.append(f"{u.minumero}: {u.name}")
        return {"numerosDestino": res}

#mensajeria/enviar?mialias=cpaz&aliasdestino=lmunoz&texto=hola

@app.get("/billetera/pagar")
def enviar_pago(
minumero: str | None = None,numerodestino: str | None = None,valor: int | None = None):
    if minumero is None or numerodestino is None or valor is None:
        return {"mensaje": "Faltan datos"}
    else:
        for u in DB:
            if u.minumero == minumero:
                u.monto=u.monto+valor
                print(u.monto)
                for c in u.numerosDestino:
                    if c == numerodestino:
                        fecha = date.today().strftime('%d/%m/%Y')
                        BD_Operaciones.append(Operacion(minumero=minumero, numeroDestino=numerodestino, fecha=fecha, valor=valor))
                        return {"mensaje": f"Realizado en {fecha}"}
                    
            
        return {"mensaje": "No se pudo pagar"}


@app.get("/billetera/historial")
def obtener_historial(minumero: str | None = None):
    cuenta = None
    for c in DB:
        if c.minumero == minumero:
            cuenta = c
            break

    if not cuenta:
        return {"Mensaje": []}
    
    saldo = cuenta.monto
    operaciones = []
    historial=[]
    for op in BD_Operaciones:
        if op.minumero == minumero or op.numeroDestino == minumero:
            operaciones.append(op)

    historial.append(f"Saldo de {cuenta.name}: {saldo}, Operaciones de {cuenta.name}:")
    #historial = f"Saldo de {cuenta.name}: {saldo}, Operaciones de {cuenta.name}: "
    for operacion in operaciones:
        if operacion.minumero == minumero:
             historial.append(f"Pago realizado de {operacion.valor} a {operacion.numeroDestino}, ")
        else:
            for cuenta in DB:
                if cuenta.minumero == operacion.minumero:
                    nombre_propietario = cuenta.name
                    historial.append( f"Pago recibido de {operacion.valor} de {nombre_propietario} ")
    
    return historial

@app.get("/")
async def root():
    return {":)"}


