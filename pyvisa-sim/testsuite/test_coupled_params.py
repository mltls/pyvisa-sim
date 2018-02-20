import os

from pyvisa.testsuite import BaseTestCase
import visa

PACKAGE = os.path.dirname(__file__)


class TestCoupledParams(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        path = os.path.join(PACKAGE, 'funcgen.yaml')
        cls.rm = visa.ResourceManager(path+'@sim')

    def test_coupled_params(self):
        rname = 'GPIB::1::INSTR'
        inst = self.rm.open_resource(rname, read_termination='\n',
                                     write_termination='\n')
        q = inst.query('*IDN?')
        self.assertEqual(q, 'mock funcgenerator')

        inst.query('AMP 0')
        self.assertEqual(float(inst.query('MIN?')),
                         0.0)
        self.assertEqual(float(inst.query('MAX?')),
                         0.0)
        inst.query('AMP 19')
        self.assertEqual(float(inst.query('MIN?')),
                         -19.0)
        self.assertEqual(float(inst.query('MAX?')),
                         19.0)
        inst.query('OFS 10')
        inst.query('AMP 5')
        self.assertEqual(float(inst.query('MIN?')),
                         5.0)
        self.assertEqual(float(inst.query('MAX?')),
                         15.0)

        inst.query('MAX 10')
        self.assertEqual(float(inst.query('OFS?')),
                         7.5)

        self.assertEqual(float(inst.query('AMP?')),
                         2.5)
        inst.query('MIN -10')
        self.assertEqual(float(inst.query('OFS?')),
                         0.0)

        self.assertEqual(float(inst.query('AMP?')),
                         10.0)
