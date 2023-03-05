<?php
trait MyTrait {
    protected $attr = self::class . 'Test';

    public function test() {
        echo $this->attr, PHP_EOL;
    }
}

class A {
    use MyTrait;
}

class B {
    use MyTrait;
}

(new A())->test();
(new B())->test();
?>