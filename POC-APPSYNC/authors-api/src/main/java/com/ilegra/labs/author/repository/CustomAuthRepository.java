package com.ilegra.labs.author.repository;

import java.util.List;

public interface CustomAuthRepository {
    List<AuthorEntity> query(List<String> ids);
}
