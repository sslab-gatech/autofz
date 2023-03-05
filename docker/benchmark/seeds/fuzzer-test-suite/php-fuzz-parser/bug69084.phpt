<?php

trait Foo {
    abstract public function doStuff();

    public function main() {
        $this->doStuff();
    }
}

class Bar {
    use Foo {
        Foo::doStuff as doOtherStuff;
    }

    public function doStuff() {
        var_dump(__FUNCTION__);
    }
}

$b = new Bar();
$b->main();

?>