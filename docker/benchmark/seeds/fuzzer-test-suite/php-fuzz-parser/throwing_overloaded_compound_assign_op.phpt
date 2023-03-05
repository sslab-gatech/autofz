<?php

class Test {
    public function __get($k) {
        $this->$k = 42;
        return 0;
    }
}

$test = new ArrayObject;
$test[0] = 42;
try {
    $test[0] %= 0;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test);

$test2 = new Test;
try {
    $test2->prop %= 0;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test2);

?>