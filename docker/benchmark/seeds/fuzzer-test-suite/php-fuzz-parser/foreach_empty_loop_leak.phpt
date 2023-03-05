<?php

class Foo implements IteratorAggregate {
    public function getIterator() {
        return new ArrayIterator([]);
    }
    public function __destruct() {
        throw new Exception;
    }
}

try {
    foreach (new Foo as $x);
} catch (Exception $e) {
    echo "Exception caught\n";
}

?>