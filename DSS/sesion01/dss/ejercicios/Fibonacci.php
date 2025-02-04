<?php
    namespace dss\ejercicios;
    class Fibonacci{
        private $secuencia;
        public function __construct(){
            $this->secuencia = [];
            $this->secuencia[0] = 0;
            $this->secuencia[1] = 1;
            for($i = 2; $i < 10; $i++)
                $this->secuencia[$i] = $this->secuencia[$i - 1] + $this->secuencia[$i - 2];
        }
        public function imprimirSecuencia(){
            echo implode(",", $this->secuencia);
        }
        function fibonacci($n){
            if($n < 0) return null;
            if(isset($this->secuencia[$n])) return $this->secuencia[$n];
            $ultimo = count($this->secuencia) - 1;
            for($i = $ultimo; $i <= $n; $i++) $this->secuencia[$i] = $this->secuencia[$i - 1] + $this->secuencia[$i - 2];
            return $this->secuencia[$n];
        }
    }
?>