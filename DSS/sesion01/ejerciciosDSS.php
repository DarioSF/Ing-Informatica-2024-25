<?php
    $saludo = "¡Hola Mundo!\n";
    echo $saludo;    
    $ejdiv = "Ejercicio división\n";
    echo $ejdiv;
    function ejdivision($num, $den){
        if($den == 0) return null;
        return $num / $den;
    }
    $res1 = ejdivision(5,2);
    $res2 = ejdivision(7,0);
    echo $res1 . "\n";
    var_dump($res2);
    $ejcad = "Ejercicio cadenas\n";
    echo $ejcad;
    function invertirCadena($cadena){
        $resultado = "";
        for($indice = strlen($cadena); $indice >= 0; $indice--){
            $resultado .= $cadena[$indice];
        }
        return $resultado;
    }
    $cadena = "hola";
    $invertida = invertirCadena($cadena);
    echo $invertida . "\n";
    $ejord = "Ejercicio ordenar\n";
    echo $ejord;
    function ordenacionBurbuja($arrayOrdenar){
        $resultado = $arrayOrdenar;
        for($indice = 1; $indice < count($resultado); $indice++){
            for($indice2 = 0; $indice2 < $indice; $indice2++){
                if($resultado[$indice2] > $resultado[$indice2 + 1]){
                    $temp = $resultado[$indice2];
                    $resultado[$indice2] = $resultado[$indice2 + 1];
                    $resultado[$indice2 + 1] = $temp;
                }
            }
        }
        return $resultado;
    }
    $arrayOrdenar = [3,1,2,5,6,4];
    print_r($arrayOrdenar);
    $arrayOrdenado = ordenacionBurbuja($arrayOrdenar);
    print_r($arrayOrdenado);
    $ejfib = "Ejercicio fibonacci\n";
    echo $ejfib;
    function fibonacci($n){
        if($n < 0) return null;
        if($n === 0) return 0;
        if($n === 1) return 1;
        $f0 = 0;
        $f1 = 1;
        for($i = 2; $i <= $n; $i++){
            $fn = $f0 + $f1;
            $f0 = $f1;
            $f1 = $fn;
        }
        return $fn;
    }
    echo fibonacci(10) . "\n";
    $ejfec = "Ejercicio fechas\n";
    echo $ejfec;
    function proximoMes(){
        $fecha = new DateTime();
        $fecha->modify('+1 month');
        return $fecha->format('d/m/Y');
    }
    echo proximoMes() . "\n";
?>