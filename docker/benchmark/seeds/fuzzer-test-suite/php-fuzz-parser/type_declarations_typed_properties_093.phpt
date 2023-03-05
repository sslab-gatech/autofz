<?php

class Test {
    public int $prop;
}

$name = new class {
    public function __toString() {
        return 'prop';
    }
};

$test = new Test;
$ref = "foobar";
try {
    $test->$name =& $ref;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test);

?>