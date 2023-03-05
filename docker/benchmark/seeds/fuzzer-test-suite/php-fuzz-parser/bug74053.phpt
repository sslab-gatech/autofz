<?php
class b {
    function __destruct() {
    echo "b::destruct\n";
    }
}
class a {
    static $b;
    static $new;
    static $max = 10;
    function __destruct() {
    if (self::$max-- <= 0) return;
    echo "a::destruct\n";
    self::$b = new b;
    self::$new[] = new a;
    }
}
new a;
?>