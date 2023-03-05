<?php

// Taken from bug #78989.

class X {
    function method($a): A {}
}
trait T {
    function method($r): B {}
}
class U extends X {
    use T;
}

?>