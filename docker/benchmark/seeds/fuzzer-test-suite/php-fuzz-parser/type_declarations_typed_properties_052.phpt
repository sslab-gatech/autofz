<?php

eval(<<<'EOF'
class A {
    public A      $a1;
    public \B     $b1;
    public Foo\C  $c1;
    public ?A     $a2;
    public ?\B    $b2;
    public ?Foo\C $c2;
}
EOF
);
$obj = new A;
var_dump($obj);
?>