<?php

trait T {
    private static function method() {
        static $x;
        if ($x === null) $x = new stdClass;
        return $x;
    }

    public static function method2() {
        return self::method();
    }
}

class C {
    use T;
}

var_dump(C::method2());

class D extends C {
    use T;
}

var_dump(D::method2());

?>