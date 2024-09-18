select
    f.film_id,
    f.title,
    string_agg(a.actor_name, ',') as actors
from
    {{ ref('films') }} f
join
    {{ ref('film_actors') }} fa
    on  f.film_id = fa.film_id
join
    {{ ref('actors') }} a
    on fa.actor_id = a.actor_id
group by
    f.film_id, f.title
