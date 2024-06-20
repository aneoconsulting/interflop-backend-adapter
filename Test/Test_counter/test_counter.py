

import pytest
import re
import subprocess
import sys
import os 

class Test_front():

    # executable = "${EXECUTABLE}"
    # tool = "${PINTOOL}"
    # pin = "${PIN}"
    # executable_verificarlo = "${EXECUTABLE2}"
    
    counterModes = ["0", "1", "2"]

    precisions = ["float", "double"]
    operations = ["add", "sub", "mul", "div", "fma"]
    modes = ["scalar", "simd"]

    backend =["libinterflop_ieee.so", "libinterflop_mca.so", "libinterflop_mca_int.so", "libinterflop_bitmask.so", "libinterflop_cancellation.so", "libinterflop_vprec.so"]

    verificarlo = "@VERIFICARLO_EXECUTABLE@"
    verrou = "@VERROU_EXECUTABLE@"
    pin = "@PIN_EXECUTABLE@"
    lib = "@LIB@"

    new_back = "@BACKEND_VERIFICARLO@"
    
    
    def launch_PENE(self, prec, op, mode, nLoop, a, b):

        cmdLine = ("{pin} -t {tool} -fp-replace 5 -counter_mode 1 -- {executable} {prec} {operation} {mode} {nLoop} {a} {b}").format(pin = self.pin, 
                                                                              tool = self.lib,
                                                                              executable = self.verrou,
                                                                              prec = prec,
                                                                              operation = op,
                                                                              mode = mode,
                                                                              nLoop = nLoop,
                                                                              a=a,
                                                                              b=b)
        
        
        out = subprocess.run(cmdLine.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        output = out.stdout.decode('utf-8')
        print("Output", output)

        # p = r"\A=*[\r\n]{1,2}\s*?PENE: Pin Enabled Numerical Exploration\s*?[\r\n]{1,2}=*[\r\n]{1,2}"
        p = r"Result : "
        assert re.search(p, output) is not None, f"échec de lancement de commande de PENE"

        return output
    
    def launch_verrou(self, prec, op, mode, nLoop, a, b):
        
        cmdLine = ("valgrind --tool=verrou --count-op=yes {verrou} {prec} {operation} {mode} {nLoop} {a} {b}").format(verrou = self.verrou, 
                                                                                                                    prec = prec,
                                                                                                                    operation = op,
                                                                                                                    mode = mode,
                                                                                                                    nLoop = nLoop,
                                                                                                                    a=a,
                                                                                                                    b=b)
        out = subprocess.run(cmdLine.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        output = out.stdout.decode('utf-8')

        p = r"Verrou, Check floating-point rounding errors"
        assert re.search(p, output) is not None, f"échec de lancement de commande {cmdLine}"

        return output

    
    def launch_verificarlo(self, prec, op, mode, nLoop, a, b):

        command = ("VFC_BACKENDS=\"{back} --count-op\" {verificalo} {prec} {operation} {mode} {nLoop} {a} {b}").format(back=self.new_back,
                                                                                                        verificalo=self.verificarlo,
                                                                                                        prec = prec,
                                                                                                        operation = op,
                                                                                                        mode = mode,
                                                                                                        nLoop = nLoop,
                                                                                                        a=a,
                                                                                                        b=b)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        output, error = process.communicate()

        # Afficher la sortie standard
        output_str = output.decode("utf-8")
        print(output_str)

        p = r"loaded backend"
        assert re.search(p, output_str) is not None, f"échec de lancement de commande"

        return output_str

    def get_Nbrop_PENE(self, pattern, prec, op, mode):

        regex = prec + r" *?" + op + r" *?" + mode + r" *?(?P<value>\d+)"
        if op == "sub":
            regex = prec + r" *?add *?" + mode  + r" *?(?P<value>\d+)"

        p=re.compile(regex)
        assert re.search(p, pattern)
        res=p.search(pattern)

        return float(res.group("value"))
    
    def get_Nbrop_verrou(self, pattern, op):

        add_sub = 0
        regex = op + r" *?(?P<value>\d+)" 
        if (op=="add" or op=="sub"):
            if (op=="add"):
                regex2 = "sub" + r" *?(?P<value2>\d+)" 
                p=re.compile(regex2)
                assert re.search(p, pattern)
                res=p.search(pattern)
            else :
                regex2 = "add" + r" *?(?P<value2>\d+)" 
                p=re.compile(regex2)
                assert re.search(p, pattern)
                res=p.search(pattern)

            add_sub=float(res.group("value2"))

        p=re.compile(regex)
        assert re.search(p, pattern)
        res=p.search(pattern)

        return float(res.group("value"))+add_sub
    
    def get_Nbrop_verificarlo(self, pattern, op):

        add_sub=0
        regex = r" *" + op + "=" +r"(?P<value>\d+)"
        if(op=="add" or op=="sub"):
            if (op=="add"):
                regex2 = r" *" + "sub" + "=" +r"(?P<value2>\d+)"
                p=re.compile(regex2)
                assert re.search(p, pattern)
                res=p.search(pattern)
            else :
                regex2 = r" *" + "add" + "=" +r"(?P<value2>\d+)"
                p=re.compile(regex2)
                assert re.search(p, pattern)
                res=p.search(pattern)

            add_sub=float(res.group("value2"))

        p=re.compile(regex)   
        assert re.search(p, pattern)
        res=p.search(pattern) 

        return float(res.group("value"))+add_sub
    
    
    @pytest.mark.parametrize("prec, op, mode, nLoop, a, b", [
            ("float", "mul", "scalar", 2, 2, 2),   
            ("float", "sub", "scalar", 10, 2, 2),    
            # ("double", "mul", "scalar", 10, 2, 2), 
            # ("double", "mul", "scalar", 10, 2, 2), 
    ])
    def test_Nbr_Op(self, prec, op, mode, nLoop, a, b):
        output_PENE = self.launch_PENE(prec, op, mode, nLoop, a, b)
        # output_verrou = self.launch_verrou( prec, op, mode, nLoop, a, b)
        output_verificarlo = self.launch_verificarlo( prec, op, mode, nLoop, a, b)

        nb_op_Pene=self.get_Nbrop_PENE(output_PENE, prec, op, mode)
        # nb_op_Verrou=self.get_Nbrop_verrou(output_verrou, op)
        nb_op_Vericarlo=self.get_Nbrop_verificarlo(output_verificarlo, op)

        # assert nb_op_Verrou==nLoop, \
        #     f"Verrou have note the number of instruments required"
        assert nb_op_Vericarlo==nLoop, \
            f"Verificarlo have note the number of instruments required"
        assert nb_op_Pene==nLoop, \
            f"PENE have note the number of instruments required"

    
if __name__ == "__main__":
    pytest.main()
