package com.ilegra.labs.book.repository;

import org.springframework.data.repository.Repository;
import java.util.List;

@org.springframework.stereotype.Repository
public interface BookRepository extends Repository<BookEntity, String> {
    List<BookEntity> findByAuthorIdIn(List<String> authorIds);

    List<BookEntity> findByIsDeletedFalse();

    BookEntity findById(String id);
}
