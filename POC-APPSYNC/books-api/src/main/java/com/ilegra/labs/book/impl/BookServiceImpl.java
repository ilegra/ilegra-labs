package com.ilegra.labs.book.impl;

import com.ilegra.labs.book.contract.v1.Book;
import com.ilegra.labs.book.contract.v1.BookService;
import com.ilegra.labs.book.repository.BookEntity;
import com.ilegra.labs.book.repository.BookRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
class BookServiceImpl implements BookService {
    @Autowired
    private BookRepository bookRepository;

    @Override
    public List<Book> query(List<String> authorIds) {
        List<BookEntity> entities = (authorIds.size() == 0) ? bookRepository.findByIsDeletedFalse() : bookRepository.findByAuthorIdIn(authorIds);

        return Optional
                .of(entities)
                .orElse(new ArrayList<>())
                .stream()
                .map(entity ->new Book(entity.getId(), entity.getAuthorId(), entity.getTitle(), String.valueOf(entity.getYear()), entity.getIsbn()))
                .toList();

    }

    @Override
    public Book findById(String id) {
        BookEntity  entity =  bookRepository.findById(id);

        if (!Optional.ofNullable(entity.getId()).isPresent())
            return new Book();

        return new Book(entity.getId(), entity.getAuthorId(), entity.getTitle(), String.valueOf(entity.getYear()), entity.getIsbn());
    }
}
