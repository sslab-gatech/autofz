<?php

class Foo {
    public static int $bar = PHP_INT_MAX;
};

try {
    Foo::$bar++;
} catch(TypeError $t) {
    var_dump($t->getMessage());
}

var_dump(Foo::$bar);

try {
    Foo::$bar += 1;
} catch(TypeError $t) {
    var_dump($t->getMessage());
}

var_dump(Foo::$bar);

try {
    ++Foo::$bar;
} catch(TypeError $t) {
    var_dump($t->getMessage());
}

var_dump(Foo::$bar);

try {
    Foo::$bar = Foo::$bar + 1;
} catch(TypeError $t) {
    var_dump($t->getMessage());
}

var_dump(Foo::$bar);

?>