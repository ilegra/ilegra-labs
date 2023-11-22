package com.ilegra.labs.author.impl;

import com.ilegra.labs.author.contract.v1.Author;
import com.ilegra.labs.author.contract.v1.AuthorService;
import com.ilegra.labs.author.repository.AuthorEntity;
import com.ilegra.labs.author.repository.AuthorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
class AuthorServiceImpl implements AuthorService {
    @Autowired
    private AuthorRepository authorRepository;

    @Override
    public Author findBy(String id) {
        if (!Optional.of(id).isPresent())
            return new Author();
        AuthorEntity entity = authorRepository.findById(id);

        return new Author(entity.getId(), entity.getName(), convertToStringFrom(entity.getBirthDate()));
    }

    @Override
    @Transactional
    public List<Author> query(List<String> ids) {
        List<AuthorEntity> authorEntities =  (ids.isEmpty()) ?  authorRepository.findAll() : authorRepository.query(ids);

        return Optional
                .of(authorEntities)
                .orElse(new ArrayList<>())
                .stream()
                .map(authorEntity -> new Author(authorEntity.getId(), authorEntity.getName(), convertToStringFrom(authorEntity.getBirthDate())))
                .collect(Collectors.toList());
    }

    private String convertToStringFrom(Date date) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy");
        Instant instant = date.toInstant();
        LocalDateTime  ldt = instant.atZone(ZoneId.of("UTC")).toLocalDateTime();

        return ldt.format(formatter);
    }

}
