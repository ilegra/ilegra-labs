package com.ilegra.labs.author.repository;

import org.springframework.data.repository.Repository;
import java.util.List;

@org.springframework.stereotype.Repository
public interface AuthorRepository extends Repository<AuthorEntity, String>, CustomAuthRepository {

    AuthorEntity findById(String id);

    List<AuthorEntity> findAll();

}
