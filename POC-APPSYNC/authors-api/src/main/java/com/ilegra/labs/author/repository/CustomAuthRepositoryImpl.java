package com.ilegra.labs.author.repository;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.apache.logging.log4j.util.Strings;

import java.util.List;
import java.util.stream.Collectors;


class CustomAuthRepositoryImpl implements CustomAuthRepository {
    @PersistenceContext
    private EntityManager entityManager;

    /**
     * This is to guarantee that for every existent id requested a given record is returned
     * For duplicated ids, using a simple select in clause will not work
     * since standard SQL will consider the input list as a "Set", removing the duplicates
     */
    public List<AuthorEntity> query(List<String> ids) {
        List<String> insertStatements  = ids.stream().map( id -> "insert into author_temp(id) values ('%s');".formatted(id)).collect(Collectors.toList());

        String tempTable  =
                """
                CREATE MEMORY LOCAL TEMPORARY TABLE author_temp (id VARCHAR);       
                %s
                """.formatted(Strings.join(insertStatements, ';'));
        entityManager.createNativeQuery(tempTable).executeUpdate();

        String query = """
                select a.id,
                       a.name,
                       birth_date 
                from author a
                inner join author_temp aut  on (a.id = aut.id)
                where a.id in ( %s );
                """.formatted(wrapWithQuotesAndJoin(ids));

        return entityManager.createNativeQuery(query, AuthorEntity.class).getResultList();
    }

    private String wrapWithQuotesAndJoin(List<String> strings) {
        return strings.isEmpty() ? "" : "'" + String.join("', '", strings) + "'";
    }

}
