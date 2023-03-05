<?php

interface I {
  public function example($a, $b, $c);
}
class A implements I {
  public function example($a, $b = null, $c = null) { } // compatible with I::example
}
class B extends A {
  public function example($a, $b, $c = null) { } // compatible with I::example
}

?>