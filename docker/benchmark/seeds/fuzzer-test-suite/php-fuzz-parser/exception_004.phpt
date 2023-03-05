<?php

class Foo { }

try {
    throw new Foo();
} catch (Foo $e) {
    var_dump($e);
}

?>