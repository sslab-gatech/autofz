<?php
function foo(...$args) {
  echo __FUNCTION__ . "\n";
  var_dump($args);
}
foo(
  'function',
  'bar',
);

class Foo
{
  public function __construct(...$args) {
    echo __FUNCTION__ . "\n";
    var_dump($args);
  }

  public function bar(...$args) {
    echo __FUNCTION__ . "\n";
    var_dump($args);
  }

  public function __invoke(...$args) {
    echo __FUNCTION__ . "\n";
    var_dump($args);
  }
}

$foo = new Foo(
  'constructor',
  'bar',
);

$foo->bar(
  'method',
  'bar',
);

$foo(
  'invoke',
  'bar',
);

$bar = function(...$args) {
  echo __FUNCTION__ . "\n";
  var_dump($args);
};

$bar(
  'closure',
  'bar',
);

# Make sure to hit the "not really a function" language constructs
unset($foo, $bar,);
var_dump(isset($foo, $bar,));
?>