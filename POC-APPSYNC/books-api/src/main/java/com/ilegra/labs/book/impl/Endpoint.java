package com.ilegra.labs.book.impl;


import com.ilegra.labs.book.contract.v1.Book;
import com.ilegra.labs.book.contract.v1.BookService;
import org.apache.logging.log4j.util.Strings;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.swing.text.html.Option;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/books/v1")
public class Endpoint {

    @Autowired
    private BookService bookService;

    @GetMapping(path = "/{id}", produces = "application/json")
    public ResponseEntity<Book> queryById(@PathVariable(name = "id") String id) {
        Book book = bookService.findById(id);

        return  (Optional.ofNullable(book).isEmpty()) ? ResponseEntity.notFound().build() : ResponseEntity.ok().body(book);

    }
    @GetMapping(produces = "application/json")
    public ResponseEntity<List<Book>> queryBooks(@RequestParam(name = "authorIds", defaultValue = "", required = false) String authorIds) {
        List<Book> books =  bookService.query(Strings.isBlank(authorIds) ? List.of() : List.of(authorIds.split(",")));

        return ResponseEntity.ok().body(books);
    }

}
