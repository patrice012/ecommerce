import os
import random
from django.utils.timezone import now as timezone_now
from django.utils.text import slugify


def user_directory_path(instance, filename):
# file will be uploaded to MEDIA_ROOT/product_name/<filename>
    # print(instance.product_file.product)
    return '{0}/{1}'.format(instance.product_file, filename)


def upload_to(instance, filename):
    time = timezone_now()
    file_name, filename_ext = os.path.splitext(filename)
    date = slugify(instance.create).split('-')
    date_pop = date.pop()

    return "%s-%s%s" % (
        slugify(instance.name),
        date,
        filename_ext.lower(),)



def slugify_instance_title(instance, save = False, new_slug = None):
    klass = instance.__class__
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    qs = klass.objects.all().filter(slug = slug).exclude(id = instance.id)
    if qs.exists():
        rand_int = random.randint(1_000, 100_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_title(instance, save = save, new_slug = slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance



# def _qs_last_item(qs):
#     list_index = []
#     for category in qs:
#         print("5555555555555",category.slug)
#         slug_list = category.slug.split('-')
#         # print("6666666666666",slug_list)
#         last_slug_item = slug_list[len(slug_list) - 1]
#         if  last_slug_item.isdigit():
#             list_index = list_index.append(int(last_slug_item))
#     # if last_slug_item.isdigit():
#     #     last_index = int(last_slug_item)
#             print("777777777777",last_index)
#         else:
#             last_index = 0
#         last_index = max(list_index)
#     return last_index

# def _create_new_slug(slug_list):
#     slug = ''
#     iterator = 0
#     for item in slug_list:
#         if iterator < len(slug_list) -1:
#             slug += item +'-'
#             iterator += 1
#     slug += str(slug_list[len(slug_list)-1])
#     print("888888888888",slug)
#     return slug


# def _slug_item(slug, last_index):
#     slug_list = slug.split('-')
#     last_slug_item = slug_list[len(slug_list) - 1]
#     if last_slug_item.isdigit():
#         last_slug_item = int(last_slug_item)+last_index
#         slug_list.append(last_slug_item)
#         slug_list[len(slug_list)-2] = slug_list[len(slug_list)-1]
#         slug_list.pop()
#         slug = _create_new_slug(slug_list)
#     else:
#         last_index = last_index + 1
#         slug_list.append(last_index)
#         slug = _create_new_slug(slug_list)
#     return slug


# # def _instance_save(flag):
# #     if flag:
# #         last_index = _qs_last_item(qs)
# #         slug = _slug_item(slug,last_index )
# #         print(slug)
# #         return slug



# def slugify_instance_title(instance, save = False, new_slug = None):
#     klass = instance.__class__
#     if new_slug is not None:
#         qs = klass.objects.filter(slug = new_slug).exclude(id = instance.id)
#         print("111111111111111",qs)
#         if not qs.exists():
#             slug = new_slug
#         else:
#             last_index = _qs_last_item(qs)
#             slug = _slug_item(slug,last_index )
#             print("222222222222",slug)
#             instance.slug = slug
#             if save:
#                 instance.save()

#     else:
#         slug = slugify(instance.name)
#         qs = klass.objects.filter(slug__icontains = slug).exclude(id = instance.id)
#         print("333333333333333",qs)

#         # slug = _instance_save(True)
#         if qs.exists():
#             last_index = _qs_last_item(qs)
#             slug = _slug_item(slug,last_index )
#         print("44444444444444",slug)
#         instance.slug = slug
        
#         if save:
#             instance.save()
#     return instance
























#     # def _slug_item(slug):
#     #     slug_list = slug.split('-')
#     #     last_slug_item = slug_list[len(slug_list) - 1]
#     #     if last_slug_item.isdigit():
#     #         print('yyyyyyyyyes')
#     #         last_slug_item = int(last_slug_item)+1
#     #         slug_list.append(last_slug_item)
#     #         slug_list[len(slug_list)-2] = slug_list[len(slug_list)-1]
#     #         slug_list.pop()
#     #         slug = ''
#     #         iterator = 0
#     #         for item in slug_list:
#     #             if iterator < len(slug_list) -1:
#     #                 slug += item +'-'
#     #                 iterator += 1
#     #         slug += str(slug_list[len(slug_list)-1])
#     #         slug = slug
#     #     else:
#     #         slug = slug
#     #     return slug