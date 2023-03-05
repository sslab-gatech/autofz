<?php

interface I {
  public function example();
}
class A implements I {
  public function example(): int { } // compatible with I::example
}
class B extends A {
  public function example(): string { } // compatible with I::example
}

?>