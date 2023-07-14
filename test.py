import unittest
from apis import gente_pagar,enviar_pago,obtener_historial,getCuenta
class TestSample(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_numerosDestino(self):#validamos si el usuario tiene numeros de destino
        result = gente_pagar("123")
        self.assertNotEqual(result["numerosDestino"], [])  # Diferente de vacío 
        #valida si la lista de numerosDestino es diferente a 0, si es diferente entonces tiene por eso saca true
        
        self.assertEqual(gente_pagar("21345"),{"numerosDestino":["123: Luisa", "456: Andrea"]})#valida si es igual   Equal=igual

    def test_failed_numerosDestino(self): 
        self.assertEqual(gente_pagar("3842")["numerosDestino"], [])#valida si es igual   Equal=igual
    
    def test_failed_enviar_pago(self):
        self.assertNotEqual(enviar_pago(minumero="012",numerodestino="456",valor=10)["mensaje"],{})
        self.assertEqual(enviar_pago(minumero="147",numerodestino="258",valor=20)["mensaje"],'No se pudo pagar')
    

    def test_failed_obtener_historial(self):
        self.assertDictEqual(obtener_historial(),{'Mensaje': []})
        self.assertEqual(obtener_historial()["Mensaje"],[])


    def tearDown(self):
        pass