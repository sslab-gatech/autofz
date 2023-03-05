<?php

abstract class AbstractTraversable implements Traversable {}

class NonAbstractTraversable extends AbstractTraversable implements IteratorAggregate {
    public function getIterator() {
        yield "foo";
        yield "bar";
    }
}

foreach (new NonAbstractTraversable as $value) {
    echo $value, "\n";
}

?>