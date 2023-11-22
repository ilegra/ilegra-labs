package com.ilegra.labs.book.contract.v1;

import java.util.List;

public interface BookService {

    List<Book> query(List<String> authorIds);

    Book findById(String id);
}
