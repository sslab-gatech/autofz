<?php

interface Foo extends Traversable {
}

class Example implements Foo, IteratorAggregate {
    public function getIterator() {
        return new ArrayIterator([]);
    }
}

?>
===DONE===