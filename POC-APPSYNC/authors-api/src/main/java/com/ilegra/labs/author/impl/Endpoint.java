package com.ilegra.labs.author.impl;

import com.ilegra.labs.author.contract.v1.Author;
import com.ilegra.labs.author.contract.v1.AuthorService;
import org.apache.logging.log4j.util.Strings;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("authors/v1")
public class Endpoint {

    @Autowired
    private AuthorService authorService;

    @GetMapping("/{id}")
    public ResponseEntity<Author> queryById(@PathVariable(name = "id") String id) {
        Author authors =  authorService.findBy(id);

        return Strings.isEmpty(authors.getId()) ? ResponseEntity.notFound().build() : ResponseEntity.ok().body(authors);
    }

    @GetMapping(produces = "application/json")
    public ResponseEntity<List<Author>> queryAll(@RequestParam(name = "ids", defaultValue = "", required = false)  List<String> ids) {
        List<Author> authors =  Optional.of(authorService.query(ids)).orElse(new ArrayList<>());

        return ResponseEntity.ok().body(authors);
    }
}
