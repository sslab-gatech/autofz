<?php

trait A {
    function namespace() {
        echo "Called\n";
    }
}

class C {
    use A {
        namespace as bar;
    }
}

$c = new C;
$c->bar();
$c->namespace();

?>