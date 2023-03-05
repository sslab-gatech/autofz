<?php

$c = function(){};

$scope = "AAAA";
$scope = "{$scope}BBBB";
$c->bindTo(new stdClass, $scope);

?>