<?php

class Vuln {
    public $a;
    public function __destruct() {
        unset($this->a);
        $backtrace = (new Exception)->getTrace();
        var_dump($backtrace);
    }
}

function test($arg) {
    $arg = str_shuffle(str_repeat('A', 79));
    $vuln = new Vuln();
    $vuln->a = $arg;
}

function test2($arg) {
    $$arg = 1; // Trigger symbol table
    $arg = str_shuffle(str_repeat('A', 79));
    $vuln = new Vuln();
    $vuln->a = $arg;
}

test('x');
test2('x');

?>