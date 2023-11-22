package com.ilegra.labs.author.contract.v1;

import java.util.List;

public interface AuthorService {

    Author findBy(String id);

    List<Author> query(List<String> ids);
}
