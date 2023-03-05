<?php
class C {
    public function __construct() {
        $this->p = (object)["x" => [1]];
    }
}
class E {
}
$e = new E;
$e->f = new E;
$e->f->e = $e;
$e->a = new C;
$e = null;
gc_collect_cycles();
var_dump(new C);
?>