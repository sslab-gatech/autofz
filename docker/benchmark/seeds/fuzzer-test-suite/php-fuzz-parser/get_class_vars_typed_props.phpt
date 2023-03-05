<?php

class Test {
    public static int $int1;
    public static int $int2 = 42;
    public int $int3;
    public int $int4 = 42;
}

var_dump(get_class_vars(Test::class));

?>