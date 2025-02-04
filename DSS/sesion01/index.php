<?php
    require_once 'dss/ejercicios/Fibonacci.php';
    use dss\ejercicios\Fibonacci;
    $fib = new Fibonacci();
    echo "Secuencia inicial: ";
    $fib->imprimirSecuencia();
    echo "\n";
    echo "Fibonacci de 5: " . $fib->fibonacci(5) . "\n";
    echo "Fibonacci de 12: " . $fib->fibonacci(12) . "\n";
    echo "Secuencia actualizada: ";
    $fib->imprimirSecuencia();
    echo "\n";
?>