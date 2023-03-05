<?php

class Test {
    public int $i;
}

$test = new Test;
try {
    $test->i++;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    $test->i += 1;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>