<?php

trait T {
    public function test($arg): static {
        return $arg;
    }
}

class C {
    use T;
}
class P extends C {
}

$c = new C;
$p = new P;
var_dump($c->test($c));
var_dump($c->test($p));
var_dump($p->test($p));
var_dump($p->test($c));

?>